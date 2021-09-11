import os
import json
import quinnat
import discord
import asyncio
from multiprocessing import Process

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
URBIT_URL = os.getenv('URBIT_URL')
URBIT_SHIP = os.getenv('URBIT_SHIP')
URBIT_CODE = os.getenv('URBIT_CODE')

def urbit_client():
    client = quinnat.Quinnat(
        URBIT_URL,
        URBIT_SHIP,
        URBIT_CODE
    )

    client.connect()

    return client

def groups():
    with open('groups.json', 'r') as groupfile:
            data = groupfile.read()

    return json.loads(data)

class FauxDiscordListener(discord.Client):
    @property
    def group(self):
        return self._group

    @group.setter
    def group(self, value):
        self._group = value

    @property
    def urbit_client(self):
        return self._urbit_client

    @urbit_client.setter
    def urbit_client(self, value):
        self._urbit_client = value

    async def on_message(self, message):
        if message.author == self.user:
            return
        else:
            if self.group["discord_group_id"] == message.guild.id:
                matching_channels = list(
                    filter(
                        lambda c: c["discord_channel_id"] == message.channel.id,
                        self.group["channels"]
                    )
                )

                if len(matching_channels) != 0:
                    channel = matching_channels[0]

                    self.urbit_client.post_message(
                        self.group["urbit_ship"],
                        channel["urbit_channel"],
                        {"text": "%s: %s" % (message.author.display_name, message.content)}
                    )

class FauxDiscordPoster(discord.Client):
    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        self._message = value

    async def on_ready(self):
        discord_channel = self.get_channel(self.message["channel_id"])

        result = await discord_channel.send(self.message["content"])
        await self.close()

class FauxUrbitListener():
    @property
    def group(self):
        return self._group

    @group.setter
    def group(self, value):
        self._group = value

    @property
    def urbit_client(self):
        return self._urbit_client

    @urbit_client.setter
    def urbit_client(self, value):
        self._urbit_client = value

    def run(self):
        async def urbit_action(message, _):
            if self.group["urbit_ship"] == message.host_ship:
                matching_channels = list(
                    filter(
                        lambda c: c["urbit_channel"] == message.resource_name,
                        self.group["channels"]
                    )
                )

                if len(matching_channels) != 0:
                    channel = matching_channels[0]

                    poster = FauxDiscordPoster()
                    poster.message = {"channel_id": channel["discord_channel_id"],
                                      "content": "~%s: %s" % (message.author, message.full_text)}
                    await poster.start(DISCORD_TOKEN)

        def urbit_listener(message, _):
            asyncio.run(urbit_action(message, _))

        self.urbit_client.listen(urbit_listener)

def discord_runner(group):
    listener = FauxDiscordListener()
    listener.group = group
    listener.urbit_client = urbit_client()

    listener.run(DISCORD_TOKEN)

def urbit_runner(group):
    print(group)
    listener = FauxUrbitListener()
    listener.group = group
    listener.urbit_client = urbit_client()

    listener.run()

if __name__ == '__main__':
    for group in groups():
        discord_process = Process(target=discord_runner, args=(group,))
        urbit_process = Process(target=urbit_runner, args=(group,))
        discord_process.start()
        urbit_process.start()

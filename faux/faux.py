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
    with open('../groups.json', 'r') as groupfile:
            data = groupfile.read()

    return json.loads(data)

class FauxDiscordListener(discord.Client):
    @property
    def groups(self):
        return self._groups

    @groups.setter
    def groups(self, value):
        self._groups = value

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
            matching_groups = list(
                filter(
                    lambda g: g["discord_group"] == message.guild.name,
                    self.groups)
            )
            if len(matching_groups) != 0:
                group = matching_groups[0]

                matching_channels = list(
                    filter(
                        lambda c: c["discord_channel_name"] == message.channel.name,
                        group["channels"]
                    )
                )

                if len(matching_channels) != 0:
                    channel = matching_channels[0]

                    self.urbit_client.post_message(
                        group["urbit_ship"],
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
    def groups(self):
        return self._groups

    @groups.setter
    def groups(self, value):
        self._groups = value

    @property
    def urbit_client(self):
        return self._urbit_client

    @urbit_client.setter
    def urbit_client(self, value):
        self._urbit_client = value

    def run(self):
        async def urbit_action(message, _):
            matching_groups = list(
                filter(
                    lambda g: g["urbit_ship"] == message.host_ship,
                    self.groups)
            )
            if len(matching_groups) != 0:
                group = matching_groups[0]

                matching_channels = list(
                    filter(
                        lambda c: c["urbit_channel"] == message.resource_name,
                        group["channels"]
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

def discord_runner():
    listener = FauxDiscordListener()
    listener.groups = groups()
    listener.urbit_client = urbit_client()

    listener.run(DISCORD_TOKEN)

def urbit_runner():
    listener = FauxUrbitListener()
    listener.groups = groups()
    listener.urbit_client = urbit_client()

    listener.run()

if __name__ == '__main__':
    discord_process = Process(target=discord_runner)
    urbit_process = Process(target=urbit_runner)
    discord_process.start()
    urbit_process.start()

import string
import os
import json
import quinnat
import discord
import discord.http
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
        if (not message.guild):
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
                    printable = set(string.printable)
                    author = ''.join(filter(lambda x: x in printable, message.author.name))
                    parsed = ''.join(filter(lambda x: x in printable, message.clean_content))
                    url = ''
                    if parsed.startswith("https://tenor") and not parsed.endswith(".gif"):
                        url = f'{parsed}.gif'
                    if message.reference:
                        ref_author = ''.join(filter(lambda x: x in printable, message.reference.resolved.author.name))
                        ref_parsed = ''.join(filter(lambda x: x in printable, message.reference.resolved.clean_content))
                        parsed = f'''> *({ref_author}): {ref_parsed}*

                        {parsed}'''
                    if len(message.stickers) > 0:
                        url = message.stickers[0].image.url
                    if len(message.embeds) > 0:
                        embed = message.embeds[0].to_dict()
                        try:
                            url = embed["video"]["url"]
                        except KeyError:
                            pass
                        else:
                            try:
                                url = embed["url"]
                            except KeyError:
                                parsed = parsed + json.dumps(embed, indent=2)
                    if (len(message.attachments) > 0):
                        url = message.attachments[0].url
                        result = {"text": f'__{author}__: {parsed}'}
                        self.urbit_client.post_message(
                            self.group['urbit_ship'],
                            channel["urbit_channel"],
                            result
                            )
                        if (url):
                            self.urbit_client.post_message(
                                self.group['urbit_ship'],
                                channel["urbit_channel"],
                                {
                                 "url": url
                                 }
                            )

                    else:
                        result = {"text": f'__{author}__: {parsed}'}
                        if url == f'{parsed}.gif':
                            self.urbit_client.post_message(
                                self.group["urbit_ship"],
                                channel["urbit_channel"],
                                {"url": url}
                            )

                        self.urbit_client.post_message(
                            self.group["urbit_ship"],
                            channel["urbit_channel"],
                            result
                        )


class FauxUrbitListener(discord.http.HTTPClient):
    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        self._message = value

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
            await self.static_login(DISCORD_TOKEN)
            if self.group["urbit_ship"] == message.host_ship:
                matching_channels = list(
                    filter(
                        lambda c: c["urbit_channel"] == message.resource_name,
                        self.group["channels"]
                    )
                )

                if len(matching_channels) != 0:
                    channel = matching_channels[0]

                    self.message = {"channel_id": channel["discord_channel_id"],
                                    "content": "%s" % (message.full_text)}
                    if message.author == "littel-wolfur":
                        await self.send_message(
                            channel["discord_channel_id"],
                            message.full_text)

        def urbit_listener(message, _):
            asyncio.run(urbit_action(message, _))

        while True:
            try:
                self.urbit_client.listen(urbit_listener)
            except UnicodeDecodeError:
                self.urbit_client.ship.delete()
                self.urbit_client = urbit_client()

                continue


def discord_runner(group):
    listener = FauxDiscordListener()
    listener.group = group
    listener.urbit_client = urbit_client()

    listener.run(DISCORD_TOKEN)

def urbit_runner(group):
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

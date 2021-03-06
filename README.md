# Faux

Faux is a chatbot bridge between urbit and discord. Whenever a member posts in your discord group, a bot will echo their message in your urbit group, and vice versa.

![](https://i.imgur.com/O3mPICH.png)

## Setup

### Installation

`git clone https://github.com/midsum-salrux/faux`

`cd faux`

`pip3 install .`

### Configuration

#### Environment Variables

If you get `TypeError: unsupported operand type(s) for +: 'NoneType' and 'str'`, it means that you haven't set these correctly. [You can read about how to set environment variables here](https://www.digitalocean.com/community/tutorials/how-to-read-and-set-environmental-and-shell-variables-on-linux)

##### URBIT_URL
Wherever your urbit bot is hosted. This will often be `http://localhost:8080`

##### URBIT_SHIP
Your urbit bot ship name, with no `~`. For example, `botdys-dozzod-tomdys`

##### URBIT_CODE
The `+code` of your urbit bot

##### DISCORD_TOKEN
You need to create a discord bot to self-host Faux. [Here are some instructions](https://www.freecodecamp.org/news/create-a-discord-bot-with-python/)

This environment variable is the API token of your discord bot. You can find it here:

![](https://i.imgur.com/s6k1GUt.png)

[When you create your OAuth2 URL, be sure to check these boxes](https://user-images.githubusercontent.com/45724082/141873788-dea0d195-b860-4b24-bdcb-d15c50928e4e.png)

#### groups.json

This file specifies where posts will be echoed between. Here's a sample:

```
[{"urbit_ship": "zod",
  "discord_group_id": 214365879012435876,
  "channels": [
      { "discord_channel_id": 123456789012345678,
        "urbit_channel": "general-1234" }]}]

```

##### urbit_ship

The name of the ship hosting your chat (ordinarily the same as the ship hosting your group, but if they're separate, you want the chat ship). 

No `~`

##### discord_group_id

The internal id of your discord group. You can find it from the URL

![](https://i.imgur.com/Kjnih92.png)

##### channels

A list of channels you want to sync

##### urbit_channel

The name and number of your urbit channel. You can find it from the URL

![](https://i.imgur.com/8bYCmHw.png)

##### discord_channel_id

The internal id of your discord channel. You can find it from the URL

![](https://i.imgur.com/RfEIPzk.png)

### Running

Invite your urbit bot to your urbit group, and your discord bot to your discord group, then run:

`python3 faux/faux.py`

## Support

Join `~tomdys/the-faux-shore` on urbit

## Caveats

The bot will not trigger on its own messages, and the bot will not work in chats that it hosts itself. It's best to use a separate moon for your bot.

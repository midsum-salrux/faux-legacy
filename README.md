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

##### URBIT_URL
Whenever your urbit bot is hosted. This will often be `http://localhost:8080`

##### URBIT_SHIP
Your urbit bot ship name, with no `~`. For example, `botdys-dozzod-tomdys`

##### URBIT_CODE
The `+code` of your urbit bot

##### DISCORD_TOKEN
You need to create a discord bot to self-host Faux. Here are some instructions:

https://www.freecodecamp.org/news/create-a-discord-bot-with-python/

This environment variable is the API token of your discord bot. You can find it here:

![](https://i.imgur.com/s6k1GUt.png)

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

The name of the ship hosting your group. No `~`

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

Join ~tomdys/the-faux-shore on urbit
# Faux

Faux is a chatbot bridge between urbit and discord. Whenever a member posts in your discord group, a bot will echo their message in your urbit group, and vice versa.

![](https://i.imgur.com/O3mPICH.png)

## Setup

Self-hosting is encouraged, especially for private groups, but I also run a public instance.

### Self-hosting

#### Installation

`git clone https://github.com/midsum-salrux/faux`

`cd faux`

`pip3 install .`

#### Configuration

##### Environment Variables

###### URBIT_URL
Whenever your urbit bot is hosted. This will often be `http://localhost:8080`

###### URBIT_SHIP
Your urbit bot ship name, with no `~`. For example, `botdys-dozzod-tomdys`

###### URBIT_CODE
The `+code` of your urbit bot

###### DISCORD_TOKEN
The API token of your discord bot. You can find it here:

![](https://i.imgur.com/qOGnHlc.png)

#### groups.json

This file specifies where posts will be echoed between. Here's a sample:

```
[{"urbit_ship": "zod",
  "discord_group": "My Discord Group",
  "channels": [
      { "discord_channel_name": "general",
        "discord_channel_id": 123456789012345678,
        "urbit_channel": "general-1234" }]}]
```

##### urbit_ship

The name of the ship hosting your group. No `~`

##### discord_group

The name of your discord server

##### channels

A list of channels you want to sync

##### discord_channel_name

The name of your discord channel

##### urbit_channel

The name and number of your urbit channel. You can find it from the URL

![](https://i.imgur.com/8bYCmHw.png)

##### discord_channel_id

The internal id of your discord channel. You can find it from the URL

![](https://i.imgur.com/RfEIPzk.png)

#### Running

Invite your urbit bot to your urbit group, and your discord bot to your discord group, then run:

`python3 faux/faux.py`

### Public instance

Here's how to get the public instance of Faux in your group:

1. Invite `~botdys-dozzod-tomdys` to your group
2. Click this link to invite the public discord bot to your discord group https://discord.com/api/oauth2/authorize?client_id=885566842540814356&permissions=3072&redirect_uri=https%3A%2F%2Fdiscordapp.com%2Foauth2%2Fauthorize%3F%26client_id%3D885566842540814356%26scope%3Dbot&scope=bot
3. Send me an entry for your group in groups.json format (described above) via DM to `~midsum-salrux`.
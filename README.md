# Telegram to Discord Message Bot — Forward Telegram Messages to Discord

This is a fork of [kkapuria3/Telegram-To-Discord-Forward-Bot](https://github.com/kkapuria3/Telegram-To-Discord-Forward-Bot)

## Description

Forwardgram is a free and open source, telegram to discord message bot. It enables one to forward messages from Multiple Telegram channels to one (or more) Telegram/Discord channels of your own. This python bot monitors multiple telegram channels. When a new message/entity is sent, it will parse the response and forward it to a discord channel using your own personalized bot. It will also forward the same message to your own Telegram channel.

### Main changes

1. Bot now can forward messages with multiple images and videos
2. Bot cannot re-forward messages to telegram
3. By default messages forwards only to one discord channel, but you can add more in code

### To-do list

? - dunno if i really decide to do this

- [ ] automatic ads detection ?
- [ ] multiple discord channels as default (or minimum preparation)

### Dependencies

1. Python 3.6+
2. [Anaconda Python Console](https://www.anaconda.com/products/individual) (Optional, makes pip install debugging go away, in my case i used linux terminal)
3. Create your own discord bot, add it to your server and retrive token. Follow Steps [here](https://www.writebots.com/discord-bot-token/).
4. Have a Telegram account with valid phone number

### Installing and Setup

1. Clone this repository
2. Open your choice of console (or Anaconda console) and navigate to cloned folder
3. Run Command: `python3 -m pip install -r requirements.txt`.
4. Fill out a configuration file. An example file can be found at `template-config.yaml`.

### First Run and Usage

1. Change the name of `template-config.yaml` to `config.yaml`

#### Filling `config.yml` file

* Find channel that you want forward message from (but for the debug purpose i recommend to create your own one to check if you setup everything correctly, you can create private channel for yourself), use `https://t.me/JsonDumpBot` for parsing channel id. **Important note**: you cannot use chats for forwarding to discord.
* Add your Telegram `api_id` and `api_hash` to config.yml | Read more [here](https://core.telegram.org/api/obtaining_api_id)
* Add your `discord_bot_token` to config.yml | Read more [here](https://www.writebots.com/discord-bot-token/)
* Add your `discord_1_channel` channel id. if you remove/add extra discord channels you have to update code in `discord` folder
* In discord folder, if you add new channel, you should write new message modifier, usually i use it to detect ads in posts, you can look at existing examples and write your own or just return basic message without changes.

Example of what you need to find in json dump.

```json
    "forward_from_chat": {
      "id": -1001320343625.
      ...
    }
```


#### Editing `discord` folder

- Whenever you add and delete discord channels in `config.yaml`; `discord/botRunner.py` and `discord/channelHandlers.py` will have to be updated. If you know basic python you will understand the code.

- Multiple send telegram channels in `config.yaml` can added without any code change.

### Running

Run the command `python3 main.py config.yaml`

```text
***PLEASE NOTE:  In the first time initializing the script, you will be required to validate your phone number using telegram API. This happens only at the first time (per session name).
```

### Troubleshooting

if for some reason you lost packets, turn off vpn, this was a problem for me

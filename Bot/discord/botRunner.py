import discord
from Bot.logger.log import logger
from Bot.shared.variables import *
from Bot.discord.channelHandlers import MessageModifiers, RetranslateOptions
from os import path
from shutil import rmtree
import asyncio


def check_for_ads(message):
    # if message contains tag for ads we drop it despite the channel
    if message.find("#реклама") != -1 or message.find("#Реклама") != -1:
        logger.info("Dropping message with ads")
        return FlagAds
    
    # if tag is not send, we will check message using modifiers
    # for that we need to get channel name
    with open(DirectoryTempFiles + FileTempChannelName, 'r') as f:
        channel_name = f.read()
    
    # now we check if channel has modifier
    if channel_name in MessageModifiers:
        message = MessageModifiers[channel_name](message) # apply modifier
        return message
    else:
        return FlagNoChannel


async def send_media(channel):
    if not path.exists(DirectoryTempFiles + FileTempToSend):
        logger.info("Discord runner: No media files to send")
        return

    # first we get list of files to send
    with open(DirectoryTempFiles + FileTempToSend, 'r') as f:
        files = f.readlines()
    
    # now we need to send them
    for file in files:
        file = file.strip()
        if path.exists(file):
            await channel.send(file=discord.File(file))
        else:
            logger.error(f"File {file} does not exist")


async def send_message(channel, message):
    try:
        await channel.send(message)
    except discord.errors.HTTPException:
        logger.error("Bad request, message dropped")
        return
    logger.info("Sent message")



async def start_discord_client(config):
    # Initialize the client
    intents = discord.Intents.default()
    discord_client = discord.Client(intents=intents)

    async def on_ready():
        logger.info(f'Discord runner: logged in as {discord_client.user}')

        with open(DirectoryTempFiles + FileTempChannelName, 'r') as f:
            channel_name = f.read()

        channel = discord_client.get_channel(config[RetranslateOptions[channel_name]])
        needToSendMessage = False
        # first we modify message and check if there is ads
        # for that we first need to check if there is a message to send
        if path.exists(DirectoryTempFiles + FileTempMessage):
            # if there is a message, we read it
            with open(DirectoryTempFiles + FileTempMessage, 'r') as f:
                message = f.read()
                needToSendMessage = True
        else:
            logger.info("Discord runner: No message to send")

        # now we check if message contains ads
        if needToSendMessage:
            message = check_for_ads(message)
            if message == FlagAds:
                rmtree(DirectoryTempFiles)
                await discord_client.close()

            elif message == FlagNoChannel:
                logger.error("Discord runner: Could not find modifier for channel")
                rmtree(DirectoryTempFiles)
                await discord_client.close()

        # if message is ok, we first send media
        try:
            await send_media(channel)
        except discord.errors.HTTPException:
            logger.warning("Discord runner: Could not send media due it's size")
        # and then we send message
        if needToSendMessage:
            await send_message(channel, message)
        rmtree(DirectoryTempFiles)
        await discord_client.close()
        exit()

    discord_client.event(on_ready)

    await discord_client.start(config["discord_bot_token"])



def start_discord_bot(config):
    asyncio.run(start_discord_client(config))
    logger.info("Discord bot ended normally")

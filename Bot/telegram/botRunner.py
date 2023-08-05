from telethon import TelegramClient, events, errors
from telethon.tl.types import InputChannel, MessageMediaPhoto, MessageMediaDocument
from os import path
from random import randint
from Bot.logger.log import logger
from Bot.shared.variables import *
from Bot.discord.botRunner import start_discord_bot
from Bot.telegram.fileOperations import *
from Bot.telegram.urlOperations import *
import multiprocessing
import asyncio


def file_race_condition(channelName):
    # First thing when we got lock, we need to check if some thread is already preparing message
    if not path.exists(DirectoryTempFiles + FileTempChannelName):
        save_channel_name_to_file(channelName)
        return "Master"
    else:  # otherwise we need to check if we are working with the same channel
        with open(DirectoryTempFiles + FileTempChannelName, 'r') as f:
            channel_name = f.read()
        if not channel_name == channelName:
            return "Wait"
        else:
            return "Slave"


async def wait_for_threads():
    global ThreadStatus
    logger.info("Telegram runner: Main thread waits everything to finish")
    CanLeave = False
    while not CanLeave:
        await asyncio.sleep(2)
        CanLeave = True
        for thread in ThreadStatus:
            if thread == "0":
                CanLeave = False


def start_telegram_client(config):
    # Create a TelegramClient instance
    client = TelegramClient(config["session_name"],
                            config["api_id"],
                            config["api_hash"])

    # Connect and log in to the Telegram client
    client.start()

    # Input Messages Telegram Channels will be stored in these empty Entities
    input_channels_entities = []
    # Iterating over dialogs and finding new entities and pushing them to our empty entities list above
    for dialog in client.iter_dialogs():
        if dialog.name in config["input_channel_names"] or dialog.entity.id in config["input_channel_ids"]:
            input_channels_entities.append(
                InputChannel(dialog.entity.id, dialog.entity.access_hash))

    if not input_channels_entities:
        logger.error(
            f"Could not find any input channels in the user's dialogs")
        return

    # Use logging and print messages on your console.
    logger.info(f"Listening on {len(input_channels_entities)} channels.")

    # multithread support
    global ThreadStatus
    ThreadStatus = list()
    lock = asyncio.locks.Lock()

    @client.on(events.NewMessage(chats=input_channels_entities))
    async def handler(event):
        threadState = "none" # one of threads become master and will send message to discord

        await lock.acquire()
        # If thread see a file with channel name, it means that some other thread is already working with it
        
        while True: # so we wait until it is finished (if we come from different channel)
            threadState = file_race_condition(event.chat.title)
            if threadState == "Master" or threadState == "Slave":
                break

            lock.release()
            logger.info("Telegram runner: thread from channel" +
                        event.chat.title + "is waiting for lock")
            await asyncio.sleep(randint(1, 15))
            await lock.acquire()

        ThreadStatus.append("0") # 0 means that thread is working
        ThreadId = len(ThreadStatus) - 1 # we need to know id of thread to know when it is finished
        lock.release()

        logger.info(f"Telegram runner: New message from {event.chat.title}:")

        parsed_response = str()
        # Initialize with the original message text
        parsed_response = event.message.message

        if not parsed_response == "":  # working with urls in message
            # first we delete all of them
            parsed_response = remove_urls_from_message(parsed_response)
            # second we find get set of unique urls that was in message
            parsed_urls = url_parser(event.message.message)
            # third we add them to the end of message
            if len(parsed_urls) > 0:
                parsed_response += '\n' + "URLs:"
                for url in parsed_urls:
                    parsed_response += '\n' + url

        # saving image from message (if there is any)
        if event.message.media:
            media = event.message.media
            # If there's a single media object, handle it directly
            if isinstance(media, MessageMediaPhoto):
                await media_save_image(media, client)
            elif isinstance(media, MessageMediaDocument) and media.document.mime_type.startswith('video/'):
                await media_save_video(media, client)

        if parsed_response != "":
            save_message_to_file(parsed_response)

        ThreadStatus[ThreadId] = "1"
        if not threadState == "Master":  # if it is not master thread, we simply leave it
            logger.info("Telegram runner: thread from channel" + event.chat.title +
                        " with id " + str(ThreadId) + " of " + str(len(ThreadStatus)-1) + " is finished")
            return
        else:
            await wait_for_threads()
            ThreadStatus.clear()

        # creating process that will run as discord bot and send message
        p = multiprocessing.Process(target=start_discord_bot, args=(config,))
        p.start()
        p.join()

    try:
        client.run_until_disconnected()
    except errors.IncompleteReadError:
        logger.warning(
            "Telegram runner: Got IncompleteReadError, client tries to restart")

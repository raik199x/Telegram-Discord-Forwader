from Bot.shared.variables import *
from os import path, mkdir
from Bot.logger.log import logger
from time import sleep
import uuid  # for unique file name


def append_to_send(fileName):
    # no need to add here message and channel name, they are will be checked anyway in discord runner
    if not path.exists(DirectoryTempFiles + FileTempToSend):
        with open(DirectoryTempFiles + FileTempToSend, 'w') as f:
            f.write(fileName)
    else:
        with open(DirectoryTempFiles + FileTempToSend, 'a') as f:
            f.write("\n" + fileName)


async def media_save_image(media, client):
    photo_path = path.join(DirectoryTempFiles, str(uuid.uuid4()) + ".jpg")
    await client.download_media(media, photo_path)
    append_to_send(photo_path)


async def media_save_video(media, client):
    video_path = path.join(DirectoryTempFiles, str(uuid.uuid4()) + ".mp4")
    await client.download_media(media, video_path)
    append_to_send(video_path)


def save_channel_name_to_file(channel_name):
    if not path.exists(DirectoryTempFiles):
        mkdir(DirectoryTempFiles)

    with open(DirectoryTempFiles + FileTempChannelName, 'w') as f:
        f.write(channel_name)


def save_message_to_file(message):
    if not path.exists(DirectoryTempFiles):
        mkdir(DirectoryTempFiles)
    file_path = DirectoryTempFiles + FileTempMessage
    with open(file_path, 'w') as f:
        f.write(message)
from Bot.shared.variables import FlagAds

def FreeGamingModifier(message):
    # Deleting self promo
    if message.find("Free Gaming - подписаться.") != -1:
        message = message.replace("Free Gaming - подписаться.", "")

    message += "\n\n#Giveaway"
    return message


def ChannelSendModifier(message):
    message += "\n\n#Admin-message"
    return message


def PesdusaModifier(message):
    message += "\n\n#Pesdusa"
    return message


def InternetModifier(message):
    if message.find("Подписывайтесь") != -1:
        return FlagAds
    if message.find("https://t.me/") != -1:
        return FlagAds
    if message.find("Отзывы") != -1:
        return FlagAds
    if message.find("Трейдер") != -1:
        return FlagAds

    message += "\n\n#Internet"
    return message

MessageModifiers = {
    "Free Gaming — Раздача игр": FreeGamingModifier,
    "channel_send": ChannelSendModifier,
    "Пездуза": PesdusaModifier,
    "!internet!": InternetModifier
}
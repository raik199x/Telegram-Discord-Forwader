from Bot.shared.variables import FlagAds

def FreeGamingModifier(message):
    # Deleting self promo
    if message.find("Free Gaming - подписаться.") != -1:
        message = message.replace("Free Gaming - подписаться.", "")

    return message


def ChannelSendModifier(message):
    return message


def PesdusaModifier(message):
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

    return message


def Pekarn9Modifier(message):
    lower_message = message.lower()
    if lower_message.find("яндекс маркет") != -1:
        return FlagAds
    if lower_message.find("яндекс.маркет") != -1:
        return FlagAds
    if lower_message.find("wildberries") != -1:
        return FlagAds
    if lower_message.find("https://t.me/") != -1:
        return FlagAds
    if lower_message.find("ozon") != -1:
        return FlagAds

    return message


MessageModifiers = {
    "Free Gaming — Раздача игр": FreeGamingModifier,
    "channel_send": ChannelSendModifier,
    "Пездуза": PesdusaModifier,
    "!internet!": InternetModifier,
    "Пекарня": Pekarn9Modifier
}

RetranslateOptions = {
    "Free Gaming — Раздача игр": "giveaway_channel",
    "channel_send": "admin_channel",
    "Пездуза": "pesduza",
    "!internet!": "internet",
    "Пекарня": "pekarn9_channel"
}
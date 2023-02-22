import os

class Config(object):

    API_ID = 4608603 #int(os.environ.get("API_ID", 12345))

    API_HASH = "1b339cc7ec86ef9ffd7d0bc8c0a2bda7" #str(os.environ.get("API_HASH", ""))

    BOT_TOKEN = "5785784298:AAEFpwZfINDSerY0o-cXFyUClsO-8iDLZ48" #str(os.environ.get("BOT_TOKEN", ""))
    
    OWNER_ID = 1729070787 #int(os.environ.get("OWNER_ID", 1428968542))

    AUTH_USERS = set(int(x) for x in "1428968542 1729070787".split())#set(int(x) for x in os.environ.get("AUTH_USERS", "").split())

    START = "Start text"#str(os.environ.get("START_TEXT", ""))

    HELP = "Help text" #str(os.environ.get("HELP_TEXT", ""))

    DONATE = "Donate text"#str(os.environ.get("DONATE_TEXT", ""))

    DONATE_LINK = "https://t.me/HeimanSupports"#str(os.environ.get("DONATE_LINK", ""))

    UPDATE_CHANNEL = "https://t.me/HeimanSupports" #str(os.environ.get("UPDATE_CHANNEL", ""))

    SUPPORT_GROUP = "https://t.me/HeimanSupport" #str(os.environ.get("SUPPORT_GROUP", ""))

    DB_URL = "mongodb+srv://heimancreatiin:heimancreatiin@cluster0.ub5udzy.mongodb.net/?retryWrites=true&w=majority" #str(os.environ.get("DB_URL", ""))
    
    DB_NAME = "test" #str(os.environ.get("DB_NAME", ""))
    
    LOG_CHANNEL = -839328944#int(os.environ.get("LOG_CHANNEL", ""))

    BROADCAST_AS_COPY = False #bool(os.environ.get("BROADCAST_AS_COPY", True))


import os

from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID", "15890589"))
API_HASH = os.getenv("API_HASH", "27fe60ebafe8a74117bfae10407925c7")
BOT_TOKEN = os.getenv("BOT_TOKEN", "7596196348:AAFhMDE1SoCxgr364u36eiVHmKN2lnN7hMs")
# BOT_TOKEN = os.getenv("BOT_TOKEN", "7911959343:AAFpk5HyxT_BA2l4D8zml7iKtmHrqsetXVw")
BOT_ID = int(os.getenv("BOT_ID", "7596196348"))
DB_NAME = os.getenv("DB_NAME", "semua12 34")
ADMIN_IDS = [1506027871]
LOG_GRUP = int(os.getenv("LOG_GRUP", -1002451566653))
AKSES_DEPLOY = list(
    map(
        int,
        os.getenv(
            "AKSES_DEPLOY",
            "1506027871",
        ).split(),
    )
)

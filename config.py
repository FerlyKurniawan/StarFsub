import os

from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID", "20409913"))
API_HASH = os.getenv("API_HASH", "7e5b7eb079ab46d84cde424962b020a0")
BOT_TOKEN = os.getenv("BOT_TOKEN", "7519209637:AAFBv-yiFpM2gkgCUxVPCvXNfALsiekjkog")
# BOT_TOKEN = os.getenv("BOT_TOKEN", "7911959343:AAFpk5HyxT_BA2l4D8zml7iKtmHrqsetXVw")
BOT_ID = int(os.getenv("BOT_ID", "7519209637"))
DB_NAME = os.getenv("DB_NAME", "FSUB")
ADMIN_IDS = [1054295664, 1259894923, 1868008472, 1871967402, 1947321138]
LOG_GRUP = int(os.getenv("LOG_GRUP", -1002156861118))
AKSES_DEPLOY = list(
    map(
        int,
        os.getenv(
            "AKSES_DEPLOY",
            "1054295664 1871967402 1259894923 1735180969 1868008472 1087819304 901367975 1947321138",
        ).split(),
    )
)

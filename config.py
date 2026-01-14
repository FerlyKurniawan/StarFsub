import os

from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID", "21810792"))
API_HASH = os.getenv("API_HASH", "a83dc6ca5cad41b93981a4fd77bfc30b")
BOT_TOKEN = os.getenv("BOT_TOKEN", "8122211209:AAGYY9-HmFRFOVjPGoQxaeiaFCJYtkdSoIk")
# BOT_TOKEN = os.getenv("BOT_TOKEN", "7911959343:AAFpk5HyxT_BA2l4D8zml7iKtmHrqsetXVw")
BOT_ID = int(os.getenv("BOT_ID", "8122211209"))
DB_NAME = os.getenv("DB_NAME", "StarFsub")
ADMIN_IDS = [7973892808, 7650122497]
LOG_GRUP = int(os.getenv("LOG_GRUP", -1002657451736))
AKSES_DEPLOY = list(
    map(
        int,
        os.getenv(
            "AKSES_DEPLOY",
            "7973892808", "7650122497"
        ).split(),
    )
)

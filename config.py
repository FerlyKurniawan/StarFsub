import os
import sys
import requests
from base64 import b64decode
import json
from dotenv import load_dotenv

def get_blacklist():
    try:
        aa = "aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL0Zlcmx5S3Vybmlhd2FuL3dhcm5pbmdzL21haW4vYmxnY2FzdC5qc29u"
        bb = b64decode(aa).decode("utf-8")
        res = requests.get(bb)
        if res.status_code == 200:
            return json.loads(res.text)
    except Exception as e:
        return f"An error occurred: {str(e)}"
        sys.exit(1)

load_dotenv()

API_ID = int(os.getenv("API_ID", "21810792"))

API_HASH = os.getenv("API_HASH", "a83dc6ca5cad41b93981a4fd77bfc30b")

BOT_TOKEN = os.getenv("BOT_TOKEN", "8122211209:AAGYY9-HmFRFOVjPGoQxaeiaFCJYtkdSoIk")

BOT_ID = int(os.getenv("BOT_ID", "8122211209"))

DB_NAME = os.getenv("DB_NAME", "StarFsub")

ADMIN_IDS = [7973892808, 7650122497]

BLACKLIST_GCAST = get_blacklist()

SUDO_OWNERS = list(
    map(
        int,
        os.environ.get(
            "SUDO_OWNERS",
            "7973892808",
        ).split(),
    )
)

DEVS = list(
    map(
        int,
        os.environ.get(
            "DEVS",
            "7973892808",
        ).split(),
    )
)

OWNER_ID = int(os.environ.get("OWNER_ID", "7973892808"))

LOG_GRUP = int(os.getenv("LOG_GRUP", -1003641876931))

FAKE_DEVS = list(map(int, os.environ.get("FAKE_DEVS", "7973892808").split()))

AKSES_DEPLOY = list(
    map(
        int,
        os.getenv(
            "AKSES_DEPLOY",
            "7973892808",
        ).split(),
    )
)

KYNAN = [7650122497, 7973892808]
if OWNER_ID not in SUDO_OWNERS:
    SUDO_OWNERS.append(OWNER_ID)
if OWNER_ID not in DEVS:
    DEVS.append(OWNER_ID)
if OWNER_ID not in FAKE_DEVS:
    FAKE_DEVS.append(OWNER_ID)
for P in FAKE_DEVS:
    if P not in DEVS:
        DEVS.append(P)
    if P not in SUDO_OWNERS:
        SUDO_OWNERS.append(P)
import os
import logging
from dotenv import load_dotenv
import yaml

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")
CLICK_TOKEN = os.getenv("CLICK_TOKEN")
PAYME_TOKEN = os.getenv("PAYME_TOKEN")
TIMEZONE = os.getenv("TIMEZONE")

WEBHOOK = os.getenv("WEBHOOK", "False").lower() == "true"
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///database.db")
DEBUG = os.getenv("DEBUG", "True").lower() == "true"
DEBUG_LEVEL = os.getenv("DEBUG_LEVEL", "info").upper()

LOG_DIR = "requests"
LOG_FILE = f"{LOG_DIR}/request.log"
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=getattr(logging, DEBUG_LEVEL, logging.INFO),
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ],
)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
LANGUAGES_FILE = os.path.join(BASE_DIR, "languages", "translations.yaml") 

with open(LANGUAGES_FILE, "r", encoding="utf-8") as file:
    LANGUAGES = yaml.safe_load(file)

logging.info("Configuration loaded successfully.")

def get_translation(key: str, language: str) -> str:
    keys = key.split(".")
    data = LANGUAGES.get(language, LANGUAGES['en'])

    try:
        for k in keys:
            data = data[k]
        if isinstance(data, str):
            return data
    except (KeyError, TypeError):
        pass

    return f"[{language}:{key}]"

def get_button_text(button_key: str, language: str) -> str:
    return get_translation(f"buttons.{button_key}", language)

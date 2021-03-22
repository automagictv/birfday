import os

from sqlalchemy.ext.declarative import declarative_base


# Sets the log file to the path provided or defaults to the tmp folder.
LOGFILE = os.environ.get("LOGFILE", "/tmp/birfdaylog")

# Database configuration
DATABASE = os.environ.get("DATABASE", "sqlite:///birfday.db")
Base = declarative_base()

# Telegram constants
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

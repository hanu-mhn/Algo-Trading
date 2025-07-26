"""
Telegram alert integration for signal alerts and error notifications.
"""
from telegram import Bot
from telegram.error import TelegramError
from .utils.logger import setup_logger

logger = setup_logger("telegram_alerts")

# Set your Telegram bot token and chat ID here
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_TELEGRAM_CHAT_ID"

def send_telegram_message(message: str):
    try:
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
        logger.info("Sent Telegram alert.")
    except TelegramError as e:
        logger.error(f"Failed to send Telegram alert: {e}")
    except Exception as e:
        logger.error(f"Unexpected error in Telegram alert: {e}")

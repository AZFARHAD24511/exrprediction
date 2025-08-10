import threading
import telebot
from config import API_TOKEN
from utils.logger import setup_logger

logger = setup_logger(__name__)

class BotRunner:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        self.stop_request = threading.Event()
        self.thread = None

    def start(self):
        if self.thread and self.thread.is_alive():
            logger.warning("Bot is already running")
            return
            
        self.stop_request.clear()
        self.thread = threading.Thread(target=self._run_bot, daemon=True)
        self.thread.start()
        logger.info("Bot started successfully")

    def stop(self, timeout=15):
        if not self.thread:
            logger.info("Bot not running")
            return
            
        self.stop_request.set()
        try:
            self.bot.stop_polling()
        except Exception as e:
            logger.error(f"Error stopping bot: {e}")
            
        self.thread.join(timeout=timeout)
        if self.thread.is_alive():
            logger.warning("Bot thread still alive after timeout")
        else:
            logger.info("Bot stopped successfully")
        self.thread = None

    def _run_bot(self):
        backoff = 1.0
        while not self.stop_request.is_set():
            try:
                self.bot.polling(none_stop=True, timeout=60)
            except Exception as e:
                logger.error(f"Polling error: {e}, retrying in {backoff}s")
                if self.stop_request.wait(timeout=backoff):
                    break
                backoff = min(backoff * 2, 30.0)
        logger.info("Bot runner exited")
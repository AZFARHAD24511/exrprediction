import os
import time
from getpass import getpass
from bot.bot_runner import BotRunner
from bot.bot_handlers import BotHandlers
from config import API_TOKEN

def main():
    # دریافت توکن از محیط یا کاربر
    token = API_TOKEN
    if not token:
        token = getpass('Enter Telegram Bot Token: ')
    
    # راه‌اندازی بات
    runner = BotRunner(token)
    handlers = BotHandlers(runner.bot)
    
    # شروع بات در پس‌زمینه
    runner.start()
    
    try:
        # نگه‌داشتن برنامه فعال
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        runner.stop()
        print("Bot stopped by user")

if __name__ == "__main__":
    main()
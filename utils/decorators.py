import time
import logging
from functools import wraps

# تنظیم لاگر برای ذخیره و نمایش خطاها
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def timer(func):
    """دکوراتور برای محاسبه زمان اجرای تابع"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        elapsed_time = time.time() - start_time
        logging.info(f"{func.__name__} executed in {elapsed_time:.4f} seconds")
        return result
    return wrapper

def error_handler(func):
    """دکوراتور برای گرفتن خطا و جلوگیری از کرش کردن برنامه"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error in {func.__name__}: {e}", exc_info=True)
            return None
    return wrapper

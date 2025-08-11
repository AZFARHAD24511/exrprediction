# utils/decorators.py
import time
import logging
from functools import wraps

logger = logging.getLogger(__name__)

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        try:
            result = func(*args, **kwargs)
            elapsed = time.time() - start
            logger.info(f"{func.__name__} finished in {elapsed:.3f}s")
            return result
        except Exception as e:
            # لاگ کامل استک‌ترَیس
            logger.exception(f"Error in {func.__name__}: {e}")
            # خیلی مهم — دوباره پرتاب کن تا فراخوان بفهمه خطا بوده
            raise
    return wrapper

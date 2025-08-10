import functools
import traceback
from utils.logger import setup_logger

logger = setup_logger(__name__)

def error_handler(func):
    """دکوراتور برای مدیریت خطاها و ثبت لاگ"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}")
            logger.error(traceback.format_exc())
            return None
    return wrapper
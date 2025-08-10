import logging
import sys

def setup_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Console Handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    
    # File Handler
    if os.getenv('ENV') == 'production':
        fh = logging.FileHandler('bot_errors.log')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    
    return logger
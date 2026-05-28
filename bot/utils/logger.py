import os
import logging
from datetime import datetime
from pytz import timezone

tz = timezone('Asia/Kolkata')    

# Setting timezone
def timetz(*args):
    return datetime.now(tz).timetuple()

logging.Formatter.converter = timetz

def get_logger(name):
    logger = logging.getLogger(name)
    os.makedirs("log", exist_ok=True)
    file_handler = logging.FileHandler("log/bot.log")
    stream_handler = logging.StreamHandler()

    formatter = logging.Formatter("[%(asctime)s - %(name)s - %(levelname)s] %(message)s",datefmt='%Y-%m-%d %I:%M:%S %p')
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    logger.setLevel(logging.INFO)

    return logger

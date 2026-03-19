import logging
import os
from logging.handlers import RotatingFileHandler
from config import LOG_ENABLED, LOG_LEVEL, LOG_DIR, LOG_FILE

LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"


def setup_logging():
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    if not LOG_ENABLED:
        root_logger.addHandler(logging.NullHandler())
        return
    os.makedirs(LOG_DIR, exist_ok=True)
    level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)
    root_logger.setLevel(level)
    formatter = logging.Formatter(LOG_FORMAT)
    file_handler = RotatingFileHandler(
        os.path.join(LOG_DIR, LOG_FILE),
        maxBytes=2_000_000,
        backupCount=5,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)

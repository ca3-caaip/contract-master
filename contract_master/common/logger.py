import os
from logging import Logger, StreamHandler, getLogger


def create_logger(log_level: str | None = None) -> Logger:
    logger = getLogger("contract-master")
    logger.addHandler(StreamHandler())
    logger.setLevel(log_level or os.getenv("LOG_LEVEL", "INFO"))
    return logger

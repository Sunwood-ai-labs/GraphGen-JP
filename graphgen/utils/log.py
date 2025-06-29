from loguru import logger
import sys

def set_logger(log_file: str, log_level: int = "INFO", if_stream: bool = True):
    # Remove all existing handlers
    logger.remove()
    # Add file handler
    logger.add(log_file, level=log_level, encoding="utf-8", enqueue=True, backtrace=True, diagnose=True)
    # Add console handler if needed
    if if_stream:
        logger.add(sys.stderr, level=log_level, enqueue=True, backtrace=True, diagnose=True)

def parse_log(log_file: str):
    with open(log_file, "r", encoding='utf-8') as f:
        lines = f.readlines()
    return lines

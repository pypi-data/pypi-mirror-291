import logging
import platform
from pathlib import Path
from datetime import datetime
from log.config import config
from concurrent_log_handler import ConcurrentRotatingFileHandler


def get_logger():
    console_log_level=logging.getLevelName(config.console_log_level)
    file_log_level=logging.getLevelName(config.file_log_level)
    log_dir=config.log_dir
    sys_name = platform.system()
    timestamp = datetime.now().strftime("%Y%m%d")
    if sys_name == "Windows":
        log_path = f"{config.log_name}_info_{timestamp}.log"
    else:
        log_path= str(Path(log_dir) / f"info_{timestamp}.log")
    file_handler = ConcurrentRotatingFileHandler(log_path, "a", 1024 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(filename)s:%(lineno)s | %(message)s'))
    log_format='%(asctime)s | %(levelname)s | %(filename)s:%(lineno)s | %(message)s'
    file_handler.setLevel(file_log_level)
    logger = logging.getLogger(config.log_name)
    if config.open_console:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level=console_log_level)
        console_handler.setFormatter(logging.Formatter(log_format))
        logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    return logger

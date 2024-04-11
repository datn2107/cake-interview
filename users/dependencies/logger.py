import os
import sys
import logging
from logging import Logger


LOGGING_FORMAT = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

class MyLogger(Logger):
    def __init__(self, name: str = "app", level=logging.INFO):
        super().__init__(name=name, level=level)

        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(LOGGING_FORMAT)

        error_file_handler = logging.FileHandler(os.getenv("ERROR_LOG_FILE"))
        error_file_handler.setLevel(logging.ERROR)
        error_file_handler.setFormatter(LOGGING_FORMAT)

        info_file_handler = logging.FileHandler(os.getenv("INFO_LOG_FILE"))
        info_file_handler.setLevel(logging.INFO)
        info_file_handler.addFilter(lambda record: record.levelno < logging.ERROR)
        info_file_handler.setFormatter(LOGGING_FORMAT)

        self.handlers = [stream_handler, error_file_handler, info_file_handler]

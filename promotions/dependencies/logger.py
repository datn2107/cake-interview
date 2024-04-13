import os
import sys
import logging
from logging import Logger


LOGGING_FORMAT = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


class MyLogger(Logger):
    def __init__(self, log_dir: str, name: str = "app", level=logging.INFO):
        super().__init__(name=name, level=level)
        os.makedirs(log_dir, exist_ok=True)

        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(LOGGING_FORMAT)

        error_file_handler = logging.FileHandler(os.path.join(log_dir, "error.log"))
        error_file_handler.setLevel(logging.ERROR)
        error_file_handler.setFormatter(LOGGING_FORMAT)

        info_file_handler = logging.FileHandler(os.path.join(log_dir, "info.log"))
        info_file_handler.setLevel(logging.INFO)
        info_file_handler.addFilter(lambda record: record.levelno < logging.ERROR)
        info_file_handler.setFormatter(LOGGING_FORMAT)

        self.handlers = [stream_handler, error_file_handler, info_file_handler]


log_dir = os.path.dirname(os.path.dirname(__file__))
app_name = os.path.basename(os.path.dirname(os.path.dirname(__file__)))

migrations_logger = MyLogger(os.path.join(log_dir, "logs", "migrate"), app_name)
web_logger = MyLogger(os.path.join(log_dir, "logs", "web"), app_name)
rabbitmq_logger = MyLogger(os.path.join(log_dir, "logs", "rabbitmq"), app_name)

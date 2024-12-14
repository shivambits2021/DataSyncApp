#app\logging_service\log_config.py
import contextvars
import sys
from logging import DEBUG, Formatter, StreamHandler, getLogger
from fastapi import Request
from graypy import GELFTCPHandler
from settings.settings import settings
from logging_service.singleton_utils import Singleton

request_context = contextvars.ContextVar("request_context")


# Create a custom log formatter with the Request object as a parameter
class RequestIDFormatter(Formatter):
    def format(self, record):
        # Access the Request object from the context variable
        request = request_context.get("request_context")
        record.trace_id = ""
        if isinstance(request, Request):
            record.trace_id = getattr(request.state, "trace_id", "")
        return super().format(record)


class LOGSetup(metaclass=Singleton):
    def __init__(self):
        # create logger
        self._logger = getLogger(name=settings.PROJECT_NAME)
        self._logger.setLevel(DEBUG)
        # Create a common formatter
        log_formatter = RequestIDFormatter(
            "[%(asctime)s] [%(thread)d][%(levelname)s] "
            "[%(filename)s] [%(funcName)s:%(lineno)d] : %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S%z",
        )

        # Create a new log Stream Handler
        log_handler = StreamHandler(sys.stdout)

        log_handler.setFormatter(log_formatter)

        self._logger.addHandler(log_handler)

        if settings.PROJECT_ENVIRONMENT != "local":
            # Create graylog file handler
            gray_log_handler = GELFTCPHandler(
                settings.GRAYLOG_HOST, settings.GRAYLOG_PORT
            )

            gray_log_handler.setFormatter(log_formatter)

            self._logger.addHandler(gray_log_handler)

    def get_logger(self):
        return self._logger


logger = LOGSetup().get_logger()

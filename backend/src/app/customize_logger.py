"""
This file is a connector for logging the uvicorn messages.
Uvicorn uses the basic python logging library, we want to use Loguru.
"""

import logging
import sys
from loguru import logger
from .config import LoggingConfig


class InterceptHandler(logging.Handler):
    loglevel_mapping = {
        50: 'CRITICAL',
        40: 'ERROR',
        30: 'WARNING',
        20: 'INFO',
        10: 'DEBUG',
        0: 'NOTSET',
    }

    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except AttributeError:
            level = self.loglevel_mapping[record.levelno]

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        log = logger.bind(request_id='app')
        log.opt(
            depth=depth,
            exception=record.exc_info
        ).log(level, record.getMessage())


class CustomizeLogger:
    @classmethod
    def make_logger(cls, config: LoggingConfig):
        return cls.customize_logging(
            filepath=config.path,
            filename=config.filename,
            level=config.level.value,
            retention=config.retention,
            rotation=config.rotation,
            format=config.format
        )

    @classmethod
    def customize_logging(cls,
                          filepath: str,
                          filename: str,
                          level: str,
                          rotation: str,
                          retention: str,
                          format: str
                          ):
        logger.remove()
        logger.add(
            sys.stdout,
            enqueue=True,
            backtrace=True,
            level=level,
            format=format
        )
        logger.add(
            f"{filepath}/{filename}",
            rotation=rotation,
            retention=retention,
            enqueue=True,
            backtrace=True,
            level=level,
            format=format
        )
        logging.basicConfig(handlers=[InterceptHandler()], level=0)
        logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]
        for _log in ['uvicorn',
                     'uvicorn.error',
                     'fastapi'
                     ]:
            _logger = logging.getLogger(_log)
            _logger.handlers = [InterceptHandler()]

        return logger.bind(request_id=None, method=None)
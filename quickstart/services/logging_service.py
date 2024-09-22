# fastapi.quickstart/services/logging_service.py

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from ..config import Config

class LoggingService:
    """
    A centralized logging service.
    """

    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """
        Get a configured logger with the specified name.

        :param name: Name of the logger.
        :return: Configured logger instance.
        """
        config = Config.get_logging_config()
        logger = logging.getLogger(name)
        if not logger.handlers:
            level = getattr(logging, config.get("level", "INFO").upper(), logging.INFO)
            logger.setLevel(level)

            formatter = logging.Formatter(config.get("format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"))

            handlers = config.get("handlers", ["console"])
            for handler_name in handlers:
                if handler_name == "console":
                    console_handler = logging.StreamHandler()
                    console_handler.setFormatter(formatter)
                    logger.addHandler(console_handler)
                elif handler_name == "file":
                    file_config = config.get("file", {})
                    filename = file_config.get("filename", "app.log")
                    max_bytes = file_config.get("max_bytes", 10485760)  # 10MB
                    backup_count = file_config.get("backup_count", 5)
                    file_handler = RotatingFileHandler(filename, maxBytes=max_bytes, backupCount=backup_count)
                    file_handler.setFormatter(formatter)
                    logger.addHandler(file_handler)
        return logger

def register_service():
    service_name = "logging_service"
    service_class = LoggingService
    return service_name, service_class

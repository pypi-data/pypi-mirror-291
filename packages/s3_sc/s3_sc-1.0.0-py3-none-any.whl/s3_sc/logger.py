"""Unit logger."""
import logging
import json
from dataclasses import dataclass, field

class JSONFormatter(logging.Formatter):
    """Custom json formatter."""

    def format(self, record: logging.LogRecord) -> str:
        """Make logs format."""
        log_record = {
            'asctime': self.formatTime(record, self.datefmt),
            'levelname': record.levelname,
            'message': record.getMessage(),
        }
        return json.dumps(log_record, ensure_ascii=False)

@dataclass
class Logging:
    """Loggin class."""

    logger_name: str
    logger: logging.Logger = field(init=False)

    def __post_init__(self) -> None:
        """Initialize the logger."""
        self.logger = logging.getLogger(self.logger_name)
        self.logger.setLevel(logging.INFO)
        formatter = JSONFormatter()
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def log(self, level: int, message: str, *args: object) -> None:
        """Log method."""
        self.logger.log(level, message, *args)

    def info(self, message: str, *args: object) -> None:
        """INFO logging level."""
        self.log(logging.INFO, message, *args)

    def debug(self, message: str, *args: object) -> None:
        """DEBUG logging level."""
        self.log(logging.DEBUG, message, *args)

    def warning(self, message: str, *args: object) -> None:
        """WARNING logging level."""
        self.log(logging.WARNING, message, *args)

    def error(self, message: str, *args: object) -> None:
        """ERROR logging level."""
        self.log(logging.ERROR, message, *args)

    def critical(self, message: str, *args: object) -> None:
        """CRITICAL logging level."""
        self.log(logging.CRITICAL, message, *args)

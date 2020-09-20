import logging
from logging.handlers import TimedRotatingFileHandler
from rich.logging import RichHandler
from mpm.core.__init__ import LOGGING_DIR, USER_DATA_DIR
from rich.console import Console
from rich.theme import Theme
from rich.style import Style

FORMATTER_FULL = logging.Formatter(
    "[%(levelname)s](%(asctime)s)LINE: %(lineno)d %(pathname)s - %(name)s %(funcName)s - %(message)s"
)
FORMATER = logging.Formatter("%(message)s")

console = Console(theme=Theme({
    "logging.level.success": Style(color="green", bold=True)
}))

def get_logging():
    SUCCESS_LEVEL = 25
    logging.addLevelName(SUCCESS_LEVEL, "SUCCESS")

    def success(self, message, *args, **kws):
        if self.isEnabledFor(SUCCESS_LEVEL):
            # Yes, logger takes its '*args' as 'args'.
            self._log(SUCCESS_LEVEL, message, args, **kws)

    logging.Logger.success = success
    return logging

logging = get_logging()

def get_console_handler(level=logging.INFO):
    console_handler = RichHandler(console=console, markup=True)
    console_handler.setFormatter(FORMATER)
    console_handler.setLevel(level)
    return console_handler


def get_file_handler(file_name, level=logging.DEBUG, formatter=None):
    file_handler = TimedRotatingFileHandler(LOGGING_DIR / file_name, when="midnight")
    file_handler.setLevel(level)
    if formatter:
        file_handler.setFormatter(formatter)
    return file_handler


def getLogger(logger_name):
    if not USER_DATA_DIR.is_dir():
        USER_DATA_DIR.mkdir()
    if not LOGGING_DIR.is_dir():
        LOGGING_DIR.mkdir()
    logging = get_logging()
    logging.basicConfig(level=logging.DEBUG)

    logger = logging.getLogger(logger_name)
    
    logger.addHandler(get_console_handler(level=logging.INFO))
    logger.addHandler(
        get_file_handler("debug.log", logging.DEBUG, formatter=FORMATTER_FULL)
    )
    logger.addHandler(
        get_file_handler("error.log", logging.ERROR, formatter=FORMATTER_FULL)
    )
    logger.propagate = False
    return logger

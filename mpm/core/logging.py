import sys
import logging
from logging.handlers import TimedRotatingFileHandler
import coloredlogs
from mpm.core.__init__ import LOGGING_DIR, USER_DATA_DIR

FORMATTER_FULL = logging.Formatter(
    "[%(levelname)s](%(asctime)s)LINE: %(lineno)d %(pathname)s - %(name)s %(funcName)s - %(message)s")


# colors = red green magenta blue yellow black cyan white
# params = bold faint 
LEVEL_STYLES = {
    'critical': {'bold': True, 'color': 'red'}, 
    'debug': {'color': 'green'}, 
    'error': {'color': 'red'}, 
    'info': {'color': 'blue'},
    'notice': {'color': 'magenta'}, 
    'spam': {'color': 'green', 'faint': True}, 
    'success': {'bold': True, 'color': 'green'}, 
    'verbose': {'color': 'blue'}, 
    'warning': {'color': 'yellow'}
}
FIELD_STYLES = {
    'asctime': {'bold': True, 'color': 'black'},
    'hostname': {'color': 'magenta'},
    'levelname': {'bold': True, 'color': 'cyan'},
    'name': {'color': 'magenta'},
    'programname': {'color': 'cyan'},
    'username': {'color': 'yellow'},
    'funcName': {'color': 'magenta'}
}

def get_logging():
    SUCCESS_LEVEL = 25
    logging.addLevelName(SUCCESS_LEVEL, "SUCCESS")
    def success(self, message, *args, **kws):
        if self.isEnabledFor(SUCCESS_LEVEL):
            # Yes, logger takes its '*args' as 'args'.
            self._log(SUCCESS_LEVEL, message, args, **kws)
    logging.Logger.success = success
    return logging


def get_console_handler(level=logging.INFO):
    logging = get_logging()
    console_handler = logging.StreamHandler()
    # console_handler.addFilter(coloredlogs.HostNameFilter())  # %(hostname)s
    # console_handler.addFilter(coloredlogs.UserNameFilter())  # %(username)s
    formatter = coloredlogs.ColoredFormatter(
        "[%(levelname)s](%(asctime)s) %(name)s %(funcName)s - %(message)s",
        level_styles=LEVEL_STYLES,
        field_styles=FIELD_STYLES
    )
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)
    return console_handler


def get_file_handler(file_name, level=logging.DEBUG, formatter=None):
    file_handler = TimedRotatingFileHandler(
        LOGGING_DIR / file_name, when='midnight')
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
    logger.addHandler(get_file_handler(
        "debug.log", logging.DEBUG, formatter=FORMATTER_FULL))
    logger.addHandler(get_file_handler(
        "error.log", logging.ERROR, formatter=FORMATTER_FULL))
    logger.propagate = False
    return logger

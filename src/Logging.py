import datetime, logging, logging.handlers, os, queue, sys, time, typing
from src import utils

LEVELS = {
    "trace": logging.DEBUG-1,
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warn": logging.WARN,
    "error": logging.ERROR,
    "critical": logging.CRITICAL
}

class BitBotFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        datetime_obj = datetime.datetime.fromtimestamp(record.created)
        return utils.iso8601_format(datetime_obj, milliseconds=True)

class Log(object):
    def __init__(self, to_file: bool, level: str, location: str):
        logging.addLevelName(LEVELS["trace"], "TRACE")
        self.logger = logging.getLogger(__name__)

        if not level.lower() in LEVELS:
            raise ValueError("Unknown log level '%s'" % level)
        stdout_level = LEVELS[level.lower()]

        self.logger.setLevel(LEVELS["trace"])

        formatter = BitBotFormatter("%(asctime)s [%(levelname)s] %(message)s")

        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(stdout_level)
        stdout_handler.setFormatter(formatter)
        self.logger.addHandler(stdout_handler)

        if to_file:
            trace_path = os.path.join(location, "trace.log")
            trace_handler = logging.handlers.TimedRotatingFileHandler(
                trace_path, when="midnight", backupCount=5)
            trace_handler.setLevel(LEVELS["trace"])
            trace_handler.setFormatter(formatter)
            self.logger.addHandler(trace_handler)

            warn_path = os.path.join(location, "warn.log")
            warn_handler = logging.FileHandler(warn_path)
            warn_handler.setLevel(LEVELS["warn"])
            warn_handler.setFormatter(formatter)
            self.logger.addHandler(warn_handler)

    def trace(self, message: str, params: typing.List=None, **kwargs):
        self._log(message, params, LEVELS["trace"], kwargs)
    def debug(self, message: str, params: typing.List=None, **kwargs):
        self._log(message, params, logging.DEBUG, kwargs)
    def info(self, message: str, params: typing.List=None, **kwargs):
        self._log(message, params, logging.INFO, kwargs)
    def warn(self, message: str, params: typing.List=None, **kwargs):
        self._log(message, params, logging.WARN, kwargs)
    def error(self, message: str, params: typing.List=None, **kwargs):
        self._log(message, params, logging.ERROR, kwargs)
    def critical(self, message: str, params: typing.List=None, **kwargs):
        self._log(message, params, logging.CRITICAL, kwargs)
    def _log(self, message: str, params: typing.Optional[typing.List],
            level: int, kwargs: dict):
        self.logger.log(level, message, *(params or []), **kwargs)

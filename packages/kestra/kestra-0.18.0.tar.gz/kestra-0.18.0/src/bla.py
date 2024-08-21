import json
from datetime import datetime, timezone
import logging
from logging import Logger

import sys


class Kestra:
    _logger: Logger = None

    def __init__(self):
        pass

    @staticmethod
    def _send(map_):
        print(Kestra.format(map_))

    @staticmethod
    def format(map_):
        return "::" + json.dumps(map_) + "::"

    @staticmethod
    def _metrics(name, type_, value, tags=None):
        Kestra._send(
            {
                "metrics": [
                    {"name": name, "type": type_, "value": value, "tags": tags or {}}
                ]
            }
        )

    @staticmethod
    def outputs(map_):
        Kestra._send({"outputs": map_})

    @staticmethod
    def counter(name, value, tags=None):
        Kestra._metrics(name, "counter", value, tags)

    @staticmethod
    def timer(name, duration, tags=None):
        if callable(duration):
            start = datetime.now()
            duration()
            Kestra._metrics(
                name,
                "timer",
                (datetime.now().microsecond - start.microsecond) / 1000,
                tags,
                )
        else:
            Kestra._metrics(name, "timer", duration, tags)

    @staticmethod
    def logger():
        if Kestra._logger is not None:
            return Kestra._logger

        logger = logging.getLogger("Kestra")

        logger.setLevel(logging.DEBUG)

        stdOut = logging.StreamHandler(sys.stdout)
        stdOut.setLevel(logging.DEBUG)
        stdOut.addFilter(lambda record: record.levelno <= logging.INFO)
        stdOut.setFormatter(JsonFormatter())

        stdErr = logging.StreamHandler(sys.stderr)
        stdErr.setLevel(logging.WARNING)
        stdErr.setFormatter(JsonFormatter())

        logger.addHandler(stdOut)
        logger.addHandler(stdErr)

        Kestra._logger = logger

        return logger


class LogFormatter(logging.Formatter):
    def formatTime(self, record, datefmt = None):
        return datetime \
            .fromtimestamp(record.created, timezone.utc) \
            .isoformat(sep="T", timespec="milliseconds") \
            .replace("+00:00", "Z")


class JsonFormatter(logging.Formatter):
    _formatter: LogFormatter = LogFormatter("%(asctime)s - %(message)s")

    @staticmethod
    def _logger_level(level: int) -> str:
        if level is logging.DEBUG:
            return "DEBUG"
        elif level is logging.INFO:
            return "INFO"
        elif level is logging.WARNING:
            return "WARN"
        elif level is logging.ERROR or level is logging.CRITICAL or level is logging.FATAL:
            return "ERROR"
        else:
            return "TRACE"

    def format(self, record: logging.LogRecord) -> str:
        result = {
            "logs" : [{
                "level": self._logger_level(record.levelno),
                "message": self._formatter.format(record),
            }]
        }

        return Kestra.format(result)


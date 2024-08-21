import logging
import unittest
from unittest import TestCase

from kestra import JsonFormatter


class TestLogger(TestCase):
    def make_record(self) -> logging.LogRecord:
        record = logging.LogRecord(
            name="logger-name",
            level=logging.DEBUG,
            pathname="/path/file.py",
            lineno=10,
            msg="%d: %s",
            args=(1, "hello"),
            func="test_function",
            exc_info=None,
        )
        record.created = 1584713566
        record.msecs = 123
        return record


    def test_execute_flow_failed(self):
        formatter = JsonFormatter()
        out = formatter.format(self.make_record())

        self.assertEqual("OK", "FAILED")

if __name__ == "__main__":
    unittest.main()

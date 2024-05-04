import logging
import sys


def setup_logger(enable=False, name="table", level=logging.INFO):
    if not enable:
        return logging.getLogger("null")

    table_logger = logging.getLogger(name)
    table_logger.setLevel(level)

    if not table_logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)

        formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)

        table_logger.addHandler(handler)

    return table_logger

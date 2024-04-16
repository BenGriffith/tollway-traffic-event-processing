import logging


def setup_logger(enable=False, name="table", level=logging.INFO, log_file="table.log"):
    if enable:
        table_logger = logging.getLogger(name)
        table_logger.setLevel(level)

        if not table_logger.handlers:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(level)

            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            file_handler.setFormatter(formatter)

            table_logger.addHandler(file_handler)

        return table_logger
    else:
        return logging.getLogger("null")

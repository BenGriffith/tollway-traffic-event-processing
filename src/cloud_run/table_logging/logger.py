import logging


def setup_logger(enable, name="table", level=logging.INFO, log_file="table.log"):
    if enable:
        logger = logging.getLogger(name)
        logger.setLevel(level)

        if not logger.handlers:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(level)

            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            file_handler.setFormatter(formatter)

            logger.addHandler(file_handler)

        return logger
    else:
        return logging.getLogger("null")

import logging
import sys


def setup_logger(verbosity):
    logger = logging.getLogger("feathercarver")
    logger.setLevel(logging.WARNING)
    handler = logging.StreamHandler(sys.stderr)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    if verbosity == 1:
        logger.setLevel(logging.INFO)
    elif verbosity == 2:
        logger.setLevel(logging.DEBUG)
    elif verbosity >= 3:
        logger.setLevel(logging.NOTSET)

    return logger

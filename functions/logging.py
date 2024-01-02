""" Script to generate the log file """
# pylint: disable=E1101
# pylint: disable=W0406
import logging
from rich.logging import RichHandler


def gen_logger(general_path):
    """ Generate the logger """
    logging.basicConfig(
        filename=f"{general_path}/logs/result.log",
        format='%(asctime)s | %(levelname)s: %(message)s',
        level=logging.INFO)
    logger = logging.getLogger()

    # Create a RichHandler for nice formatting
    rich_handler = RichHandler()
    logger.addHandler(rich_handler)

    return logger

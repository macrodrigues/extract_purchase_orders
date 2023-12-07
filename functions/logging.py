
import logging
from rich.logging import RichHandler
import datetime as dt


def gen_logger(general_path):
    logging.basicConfig(
        filename=f"{general_path}/logs/log_{dt.datetime.today()}.log",
        format='%(asctime)s | %(levelname)s: %(message)s',
        level=logging.INFO)
    logger = logging.getLogger()

    # Create a RichHandler for nice formatting
    rich_handler = RichHandler()
    logger.addHandler(rich_handler)

    return logger

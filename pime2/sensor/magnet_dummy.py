import random

from pime2.log import pime2_logger


def magnet_dummy():
    """
    Hall sensor dummy
    """
    magnet = random.randint(0, 1)
    if magnet == 0:
        pime2_logger.logging.info("No magnet detected")
        magnet = False
    else:
        pime2_logger.logging.info("Magnet detected")
        magnet = True
    return magnet

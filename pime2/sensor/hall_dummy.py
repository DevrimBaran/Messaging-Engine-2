import random
import logging


def hall_dummy():
    """
    Hall sensor dummy
    """
    magnet = random.randint(0, 1)
    if magnet == 0:
        logging.info("No magnet detected")
        magnet = False
    else:
        logging.info("Magnet detected")
        magnet = True
    return magnet

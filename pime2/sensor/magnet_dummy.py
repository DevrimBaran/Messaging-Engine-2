import random


def magnet_dummy():
    """
    Hall sensor dummy
    """
    n = random.randint(0, 1)
    if n == 0:
        magnet = False
    else:
        magnet = True
    return magnet

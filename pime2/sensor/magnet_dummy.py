import random


def magnet_dummy():
    """
    Hall sensor dummy
    """
    magnet = random.randint(0, 1)
    if magnet == 0:
        magnet = False
    else:
        magnet = True
    return magnet

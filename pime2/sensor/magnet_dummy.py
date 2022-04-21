import random

def magnet_dummy():
    n = random.randint(0,1)
    if n == 0:
        MAGNET = False
    else:
        MAGNET = True
    return MAGNET

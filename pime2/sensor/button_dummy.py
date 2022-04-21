import random

def button_dummy():
    n = random.randint(0,1)
    m = random.randint(0,1)
    if n == 1:
        BUTTON_ONE_UP = False
    else:
        BUTTON_ONE_UP = True
    if m == 1:
        BUTTON_TWO_UP = False
    else:
        BUTTON_TWO_UP = True
    return BUTTON_ONE_UP, BUTTON_TWO_UP
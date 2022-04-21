import random


def button_dummy():
    """
    Button sensor dummy
    """
    button_one_dummy = random.randint(0, 1)
    button_two_dummy = random.randint(0, 1)
    if button_one_dummy == 1:
        button_one_up = False
    else:
        button_one_up = True
    if button_two_dummy == 1:
        button_two_up = False
    else:
        button_two_up = True
    return button_one_up, button_two_up

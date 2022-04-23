import random
import logging


def button_dummy():
    """
    Button sensor dummy
    """
    button_one_dummy = random.randint(0, 1)
    button_two_dummy = random.randint(0, 1)
    if button_one_dummy == 1:
        logging.info("Button 1 down")
        button_one_up = False
    else:
        logging.info("Button 1 up")
        button_one_up = True
    if button_two_dummy == 1:
        logging.info("Button 2 down")
        button_two_up = False
    else:
        logging.info("Button 2 up")
        button_two_up = True
    return button_one_up, button_two_up

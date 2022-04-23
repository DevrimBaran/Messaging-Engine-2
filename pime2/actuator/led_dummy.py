import logging


def led_dummy(green, red):
    """
    led dummy
    """
    if green == 1 and red == 0:
        green_led = True
        red_led = False
        logging.info("Green led is on")
        return green_led, red_led
    if green == 0 and red == 1:
        green_led = False
        red_led = True
        logging.info("Red led is on")
        return green_led, red_led
    green_led = False
    red_led = False
    logging.info("No led is on")
    return green_led, red_led

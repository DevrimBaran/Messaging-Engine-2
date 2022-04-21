def actuator_dummy(green, red):
    """
    led dummy
    """
    if green == 1 and red == 0:
        green_led = True
        red_led = False
        return green_led, red_led
    if green == 0 and red == 1:
        green_led = False
        red_led = True
        return green_led, red_led
    if (green == 0 and red == 0) or (green == 1 and red == 1):
        green_led = False
        red_led = False
        return green_led, red_led

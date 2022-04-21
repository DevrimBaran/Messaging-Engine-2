#led dummy
def actuator_dummy(green, red):
    if green == 1 and red == 0:
        green_led = True
        red_led = False
        return green_led, red_led
    if green == 0 and red == 1:
        green_led = False
        red_led = True
        return green_led, red_led
    if (green == 0 and red == 0) or (green == 1 and red == 1):
        return False, False
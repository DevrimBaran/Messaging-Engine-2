# pylint: disable-all
from pime2.log.pime2_logger import pime2_logger


def actuator_dummy(green, red):
    """
    led dummy
    """
    if green == 1 and red == 0:
        green_led = True
        red_led = False
        pime2_logger().info("Green led is on")
        return green_led, red_led
    elif green == 0 and red == 1:
        green_led = False
        red_led = True
        pime2_logger().info("Red led is on")
        return green_led, red_led
    else:
        green_led = False
        red_led = False
        pime2_logger().info("No led is on")
        return green_led, red_led

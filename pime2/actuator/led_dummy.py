import logging

from pime2.actuator.actuator import DualPinActuator
from pime2.gpio_sensor_actuator.operator import DualPinOperatorArguments


class Led(DualPinActuator):
    """
    A simple led with two colors
    """

    def __init__(self, input_arguments: DualPinOperatorArguments):
        super().__init__(input_arguments)
        self.green_led = input_arguments.input_pin_1
        self.red_led = input_arguments.input_pin_2
        self.args = input_arguments

    def handle(self, trigger_args: any) -> bool:
        pass

    def open(self):
        # Will be done in Issue PIME-27 Anbindung der Aktuatoren über GPIO
        pass

    def close(self):
        # Will be done in Issue PIME-27 Anbindung der Aktuatoren über GPIO
        pass


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

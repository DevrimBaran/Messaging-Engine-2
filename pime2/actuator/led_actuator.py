# pylint: disable=import-outside-toplevel
import logging

from pime2.actuator.actuator import ActuatorType, SingleGpioActuator
from pime2.common.operator import SingleGpioOperatorArguments


class Led(SingleGpioActuator):
    """
    A simple led actuator with two colors.
    input_arguments provide a property is_test_mode.
    """

    def __init__(self, name: str, input_arguments: SingleGpioOperatorArguments):
        super().__init__(name, ActuatorType.LED, input_arguments)
        self.green_led = input_arguments.input_gpio_1
        self.args = input_arguments
        self.green_led_on = False

    def activate(self, input_arg_one: str, *input_args: str):
        led_green = bool(input_arg_one)
        if self.args.is_test_mode is False:
            from RPi import GPIO
            if led_green is True:
                # LED wird eingeschaltet
                self.green_led_on = True
                logging.info("Green led is on")
                GPIO.output(self.green_led, GPIO.HIGH)
        else:
            logging.info("Dummy led: %s", str(led_green))
            self.green_led_on = led_green

    def open(self):
        if self.args.is_test_mode is False:
            from RPi import GPIO
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.green_led, GPIO.OUT, initial=GPIO.LOW)

    def close(self):
        if self.args.is_test_mode is False:
            from RPi import GPIO
            GPIO.cleanup(self.green_led)
        self.green_led_on = False
        logging.info("Led is off")

    def is_green_led_on(self):
        """
        Getter for the variable is_green_led_on.
        """
        return self.green_led_on

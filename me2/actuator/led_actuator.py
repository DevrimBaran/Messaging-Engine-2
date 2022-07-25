# pylint: disable=import-outside-toplevel
import logging

from me2.actuator.actuator import ActuatorType, SingleGpioActuator
from me2.common.operator import SingleGpioOperatorArguments


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

    def handle(self, *input_args: str):
        # Default value for led is True
        if len(input_args) == 0:
            led_green = True
        else:
            led_green = bool(input_args[0])
        if self.args.is_test_mode is False:
            from RPi import GPIO
            if led_green is True:
                # LED wird eingeschaltet
                self.green_led_on = True
                logging.info("Led is on")
                GPIO.output(self.green_led, GPIO.HIGH)
            else:
                self.green_led_on = True
                logging.info("Led is off")
                GPIO.output(self.green_led, GPIO.LOW)
        else:
            logging.info("Dummy led: %s", str(led_green))
            self.green_led_on = led_green

    def open(self):
        if self.args.is_test_mode is False:
            from RPi import GPIO
            logging.info("Setting GPIO for led")
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.green_led, GPIO.OUT, initial=GPIO.LOW)

    def close(self):
        if self.args.is_test_mode is False:
            from RPi import GPIO
            logging.info("Cleaning GPIO ports for led")
            GPIO.cleanup(self.green_led)

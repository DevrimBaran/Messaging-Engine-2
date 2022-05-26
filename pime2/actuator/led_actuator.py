# pylint: disable=import-outside-toplevel
import logging

from pime2.actuator.actuator import ActuatorType, DualGpioActuator
from pime2.common.operator import DualGpioOperatorArguments


class Led(DualGpioActuator):
    """
    A simple led actuator with two colors.
    input_arguments provide a property is_test_mode.
    """

    def __init__(self, name: str, input_arguments: DualGpioOperatorArguments):
        super().__init__(name, ActuatorType.LED, input_arguments)
        self.green_led = input_arguments.input_gpio_1
        self.red_led = input_arguments.input_gpio_2
        self.args = input_arguments
        self.green_led_on = False
        self.red_led_on = False

    def activate(self, input_arg_one: str, input_arg_two="-1", input_arg_three="-1"):
        led_green = bool(input_arg_one)
        led_red = bool(input_arg_two)
        if self.args.is_test_mode is False:
            from RPi import GPIO
            if led_green is True:
                # LED wird eingeschaltet
                self.green_led_on = True
                logging.info("Green led is on")
                GPIO.output(self.green_led, GPIO.HIGH)
            if led_green is True:
                # LED wird eingeschaltet
                self.red_led_on = True
                logging.info("Red led is on")
                GPIO.output(self.green_led, GPIO.HIGH)
        else:
            logging.info("Green dummy led: %s, Red dummy led: %s", str(led_green), str(led_red))
            self.green_led_on = led_green
            self.red_led_on = led_red

    def open(self):
        if self.args.is_test_mode is False:
            from RPi import GPIO
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.red_led, GPIO.OUT, initial=GPIO.LOW)
            GPIO.setup(self.green_led, GPIO.OUT, initial=GPIO.LOW)

    def close(self):
        if self.args.is_test_mode is False:
            from RPi import GPIO
            GPIO.cleanup((self.green_led, self.red_led))
        self.green_led_on = False
        self.red_led_on = False
        logging.info("Led is off")

    def is_green_led_on(self):
        """
        Getter for the variable is_green_led_on.
        """
        return self.green_led_on

    def is_red_led_on(self):
        """
        Getter for the variable is_red_led_on.
        """
        return self.red_led_on

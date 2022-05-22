# pylint: disable=import-outside-toplevel
import logging

from pime2.actuator.actuator import DualPinActuator, ActuatorType
from pime2.common.operator import DualPinOperatorArguments


class Led(DualPinActuator):
    """
    A simple led with two colors
    """

    def __init__(self, input_arguments: DualPinOperatorArguments):
        super().__init__(ActuatorType.LED, input_arguments)
        self.green_led = input_arguments.input_pin_1
        self.red_led = input_arguments.input_pin_2
        self.args = input_arguments
        self.is_green_led_on = False
        self.is_red_led_on = False

    async def activate(self, led_green: bool, led_red: bool):
        if self.args.is_test_mode is False:
            from RPi import GPIO
            if led_green is True:
                # LED wird eingeschaltet
                self.is_green_led_on = True
                logging.info("Green led is on")
                GPIO.output(self.green_led, GPIO.HIGH)
            if led_green is True:
                # LED wird eingeschaltet
                self.is_red_led_on = True
                logging.info("Red led is on")
                GPIO.output(self.green_led, GPIO.HIGH)
        else:
            logging.info("Green led: " + str(led_green) + ", Red led: " + str(led_red))
            self.is_green_led_on = led_green
            self.is_red_led_on = led_red

    def open(self):
        if self.args.is_test_mode is False:
            import RPi.GPIO as GPIO
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.red_led, GPIO.OUT, initial=GPIO.LOW)
            GPIO.setup(self.green_led, GPIO.OUT, initial=GPIO.LOW)

    def close(self):
        if self.args.is_test_mode is False:
            import RPi.GPIO as GPIO
            GPIO.cleanup((self.green_led, self.red_led))
        self.is_green_led_on = False
        self.is_red_led_on = False

    def is_green_led_on(self):
        return self.is_green_led_on

    def is_red_led_on(self):
        return self.is_red_led_on

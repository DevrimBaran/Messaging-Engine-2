# pylint: disable=import-outside-toplevel
import logging
import random

from pime2.sensor.sensor import DualGpioSensor, SensorType, DualGpioOperatorArguments
from pime2.common.read_output import DualGpioCommonResult


class ButtonSensorResult(DualGpioCommonResult):
    """
    Simple type to wrap the result of a button sensor read.
    """

    def __init__(self, gpio_1_result: bool, gpio_2_result: bool):
        super().__init__(gpio_1_result, gpio_2_result)


class ButtonSensor(DualGpioSensor):
    """
    A simple button Sensor with two buttons.
    input_arguments provide a property is_test_mode.
    """

    def __init__(self, name: str, input_arguments: DualGpioOperatorArguments):
        super().__init__(name, SensorType.BUTTON, input_arguments)
        self.button_1_gpio = input_arguments.input_gpio_1
        self.button_2_gpio = input_arguments.input_gpio_2
        self.args = input_arguments

    def read(self) -> ButtonSensorResult:
        if self.args.is_test_mode is False:
            from RPi import GPIO
            # Start sensor listening
            is_button_one_up = False
            is_button_two_up = False
            if GPIO.input(self.button_1_gpio) == GPIO.LOW:
                logging.info("Button 1 up")
                is_button_one_up = True
            else:
                logging.info("Button 1 down")

            if GPIO.input(self.button_2_gpio) == GPIO.LOW:
                logging.info("Button 2 up")
                is_button_two_up = True
            else:
                logging.info("Button 2 down")
            return ButtonSensorResult(is_button_one_up, is_button_two_up)
        # Sensor dummy
        dummy_button_one_up = bool(random.randint(0, 1))
        dummy_button_two_up = bool(random.randint(0, 1))

        if dummy_button_one_up is True:
            logging.debug("Button 1 up")
        else:
            logging.debug("Button 1 down")

        if dummy_button_two_up is True:
            logging.debug("Button 2 up")
        else:
            logging.debug("Button 2 down")
        return ButtonSensorResult(dummy_button_one_up, dummy_button_two_up)

    def open(self):
        if self.args.is_test_mode is False:
            from RPi import GPIO
            # Initialising GPIO
            GPIO.setmode(GPIO.BCM)
            GPIO.setup([self.button_1_gpio, self.button_2_gpio], GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def close(self):
        if self.args.is_test_mode is False:
            from RPi import GPIO
            GPIO.cleanup((self.button_1_gpio, self.button_2_gpio))

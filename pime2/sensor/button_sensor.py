# pylint: disable=import-outside-toplevel
import logging
import random

from pime2.sensor.sensor import DualPinSensor, SensorType, DualPinOperatorArguments
from pime2.common.read_output import DualSensorResult


class ButtonSensorResult(DualSensorResult):
    """
    Simple type to wrap the result of a button sensor read.
    """

    def __init__(self, pin_1_result: bool, pin_2_result: bool):
        super().__init__(pin_1_result, pin_2_result)


class ButtonSensor(DualPinSensor):
    """
    A simple button Sensor with two buttons.
    input_arguments provide a property is_test_mode.
    """

    def __init__(self, name: str, input_arguments: DualPinOperatorArguments):
        super().__init__(name, SensorType.BUTTON, input_arguments)
        self.button_1_pin = input_arguments.input_pin_1
        self.button_2_pin = input_arguments.input_pin_2
        self.args = input_arguments

    def read(self) -> ButtonSensorResult:
        if self.args.is_test_mode is False:
            from RPi import GPIO
            # Start sensor listening
            is_button_one_up = False
            is_button_two_up = False
            if GPIO.input(self.button_1_pin) == GPIO.LOW:
                logging.info("Button 1 up")
                is_button_one_up = True
            else:
                logging.info("Button 1 down")

            if GPIO.input(self.button_2_pin) == GPIO.LOW:
                logging.info("Button 2 up")
                is_button_two_up = True
            else:
                logging.info("Button 2 down")
            return ButtonSensorResult(is_button_one_up, is_button_two_up)
        # Sensor dummy
        dummy_button_one_up = bool(random.randint(0, 1))
        dummy_button_two_up = bool(random.randint(0, 1))

        if dummy_button_one_up is True:
            logging.info("Button 1 up")
        else:
            logging.info("Button 1 down")

        if dummy_button_two_up is True:
            logging.info("Button 2 up")
        else:
            logging.info("Button 2 down")
        return ButtonSensorResult(dummy_button_one_up, dummy_button_two_up)

    def open(self):
        if self.args.is_test_mode is False:
            from RPi import GPIO
            # Initialising GPIO
            GPIO.setmode(GPIO.BCM)
            GPIO.setup([self.button_1_pin, self.button_2_pin], GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def close(self):
        if self.args.is_test_mode is False:
            from RPi import GPIO
            GPIO.cleanup((self.button_1_pin, self.button_2_pin))

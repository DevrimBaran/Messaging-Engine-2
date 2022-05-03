# pylint: disable=import-outside-toplevel
import logging
import random

from pime2.sensor.sensor import DualPinSensor, SensorType, DualPinOperatorArguments
from pime2.common.read_output import DualPinSensorReadOutput


class ButtonSensorReadOutput(DualPinSensorReadOutput):
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

    def __init__(self, input_arguments: DualPinOperatorArguments):
        super().__init__(SensorType.BUTTON, input_arguments)
        self.button_1_pin = input_arguments.input_pin_1
        self.button_2_pin = input_arguments.input_pin_2
        self.args = input_arguments

    def read(self) -> ButtonSensorReadOutput:
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
            else:
                logging.info("Button 2 down")
                is_button_two_up = True
            return ButtonSensorReadOutput(is_button_one_up, is_button_two_up)
        # Sensor dummy
        button_one_dummy = bool(random.randint(0, 1))
        button_two_dummy = bool(random.randint(0, 1))

        if button_one_dummy is False:
            logging.info("Button 1 down")
        else:
            logging.info("Button 1 up")

        if button_two_dummy is True:
            logging.info("Button 2 down")
        else:
            logging.info("Button 2 up")
        return ButtonSensorReadOutput(button_one_dummy, button_two_dummy)

    def open(self):
        if self.args.is_test_mode is False:
            from RPi import GPIO
            # Initialising GPIO
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.button_1_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(self.button_2_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def close(self):
        # TODO: Need to test GPIO.cleanup() on pi to avoid errors. Works also without cleanup.
        pass

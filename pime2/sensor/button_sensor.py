# pylint: disable=import-outside-toplevel
import logging
import random

from pime2.sensor.sensor import DualPinSensor, SensorType, DualPinOperatorArguments
from pime2.gpio_sensor_actuator.read_output import DualPinSensorReadOutput


class ButtonSensor(DualPinSensor):
    """
    A simple button Sensor with two buttons
    """

    def __init__(self, input_arguments: DualPinOperatorArguments):
        super().__init__(SensorType.BUTTON, input_arguments)
        self.button_1 = input_arguments.input_pin_1
        self.button_2 = input_arguments.input_pin_2
        self.args = input_arguments

    def read(self) -> DualPinSensorReadOutput:
        if self.args.is_test_mode is False:
            from RPi import GPIO
            # Start sensor listening
            if GPIO.input(self.button_1) == GPIO.HIGH:
                logging.info("Button 1 down")
                is_button_one_up = False
            if GPIO.input(self.button_1) == GPIO.LOW:
                logging.info("Button 1 up")
                is_button_one_up = True
            if GPIO.input(self.button_2) == GPIO.LOW:
                logging.info("Button 2 up")
                is_button_two_up = True
            if GPIO.input(self.button_2) == GPIO.HIGH:
                logging.info("Button 2 down")
                is_button_two_up = False
            return DualPinSensorReadOutput(is_button_one_up, is_button_two_up)
        # Sensor dummy
        button_one_dummy = random.randint(0, 1)
        button_two_dummy = random.randint(0, 1)
        if button_one_dummy == 1:
            logging.info("Button 1 down")
            button_one_up = False
        else:
            logging.info("Button 1 up")
            button_one_up = True
        if button_two_dummy == 1:
            logging.info("Button 2 down")
            button_two_up = False
        else:
            logging.info("Button 2 up")
            button_two_up = True
        return DualPinSensorReadOutput(button_one_up, button_two_up)

    def open(self):
        if self.args.is_test_mode is False:
            from RPi import GPIO
            # Initialising GPIO
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.button_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(self.button_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def close(self):
        # Need to test GPIO.cleanup() on pi to avoid errors. Works also without cleanup.
        pass

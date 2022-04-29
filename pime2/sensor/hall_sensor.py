import logging
import random

from pime2.sensor.sensor import SinglePinSensor, SinglePinOperatorArguments, SensorType
from pime2.gpio_sensor_actuator.read_output import SinglePinSensorReadOutput


class HallSensor(SinglePinSensor):
    """
    A simple Hall sensor (Hall sensors detect magnets)
    """
    def __init__(self, input_arguments: SinglePinOperatorArguments):
        super().__init__(SensorType.HALL, input_arguments)
        self.sensor = input_arguments.input_pin_1
        self.args = input_arguments

    def read(self) -> SinglePinSensorReadOutput:
        if self.args.is_test_mode is False:
            # start sensor listening
            from RPi import GPIO
            if GPIO.input(self.sensor) == GPIO.HIGH:
                logging.info("No Magnetic field detected")
                magnet = False
            else:
                logging.info("Magnetic field detected")
                magnet = True
            return SinglePinSensorReadOutput(magnet)
        # hall sensor dummy
        magnet = random.randint(0, 1)
        if magnet == 0:
            logging.info("No magnet detected")
            magnet = False
        else:
            logging.info("Magnet detected")
            magnet = True
        return SinglePinSensorReadOutput(magnet)

    def open(self):
        if self.args.is_test_mode is False:
            # start sensor listening
            from RPi import GPIO

            # Initialising GPIO
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.sensor, GPIO.IN)

    def close(self):
        # Need to test GPIO.cleanup() on pi to avoid errors. Works also without cleanup.
        pass

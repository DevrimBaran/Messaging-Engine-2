# pylint: disable=import-outside-toplevel
import logging
import random

from pime2.sensor.sensor import SinglePinSensor, SinglePinOperatorArguments, SensorType
from pime2.common.read_output import SingleSensorResult


class HallSensorResult(SingleSensorResult):
    """
    Simple type to wrap a single sensor measurement result
    """

    def __init__(self, result: bool):
        super().__init__(result)


class HallSensor(SinglePinSensor):
    """
    A simple Hall sensor (detect magnets)
    input_arguments provide a property is_test_mode.
    """

    def __init__(self, input_arguments: SinglePinOperatorArguments):
        super().__init__(SensorType.HALL, input_arguments)
        self.sensor = input_arguments.input_pin_1
        self.args = input_arguments

    def read(self) -> HallSensorResult:
        if self.args.is_test_mode is False:
            # start sensor listening - the conditional import is important to support non-raspi development environments
            from RPi import GPIO
            if GPIO.input(self.sensor) == GPIO.HIGH:
                logging.info("No Magnetic field detected")
                magnet = False
            else:
                logging.info("Magnetic field detected")
                magnet = True
            return HallSensorResult(magnet)
        # hall sensor dummy
        magnet = random.randint(0, 1)
        if magnet == 0:
            logging.info("No magnet detected")
            magnet = False
        else:
            logging.info("Magnet detected")
            magnet = True
        return HallSensorResult(magnet)

    def open(self):
        if self.args.is_test_mode is False:
            # start sensor listening
            # pylint-disable: import-outside-toplevel
            from RPi import GPIO

            # Initialising GPIO
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.sensor, GPIO.IN)

    def close(self):
        # TODO: Need to test GPIO.cleanup() on pi to avoid errors. Works also without cleanup.
        pass

# pylint: disable=import-outside-toplevel
import logging
import random

from pime2.sensor.sensor import SingleGpioSensor, SingleGpioOperatorArguments, SensorType
from pime2.common.read_output import SingleGpioCommonResult


class HallSensorResult(SingleGpioCommonResult):
    """
    Simple type to wrap a single sensor measurement result
    """

    def __init__(self, result: bool):
        super().__init__(result)


class HallSensor(SingleGpioSensor):
    """
    A simple Hall sensor (detect magnets)
    input_arguments provide a property is_test_mode.
    """

    def __init__(self, name: str, input_arguments: SingleGpioOperatorArguments):
        super().__init__(name, SensorType.HALL, input_arguments)
        self.sensor = input_arguments.input_gpio_1
        self.args = input_arguments

    def read(self) -> HallSensorResult:
        if self.args.is_test_mode is False:
            # start sensor listening - the conditional import is important to support non-raspi development environments
            from RPi import GPIO
            if GPIO.input(self.sensor) == GPIO.HIGH:
                logging.debug("No Magnetic field detected")
                magnet = False
            else:
                logging.debug("Magnetic field detected")
                magnet = True
            return HallSensorResult(magnet)
        # hall sensor dummy
        magnet = random.randint(0, 1)
        if magnet == 0:
            logging.debug("No magnet detected")
            magnet = False
        else:
            logging.debug("Magnet detected")
            magnet = True
        return HallSensorResult(magnet)

    def open(self):
        if self.args.is_test_mode is False:
            # start sensor listening
            from RPi import GPIO

            # Initialising GPIO
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.sensor, GPIO.IN)

    def close(self):
        if self.args.is_test_mode is False:
            from RPi import GPIO
            GPIO.cleanup(self.sensor)

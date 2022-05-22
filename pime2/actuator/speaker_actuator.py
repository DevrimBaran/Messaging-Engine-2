# pylint: disable=import-outside-toplevel
import logging

from pime2.actuator.actuator import SinglePinActuator
from pime2.common.operator import SinglePinOperatorArguments
from pime2.common.read_output import SinglePinCommonResult
from time import sleep


class Vibration(SinglePinActuator):
    """
    A simple vibration motor which vibrates
    """

    def __init__(self, input_arguments: SinglePinOperatorArguments):
        super().__init__(input_arguments)
        self.speaker = input_arguments.input_pin_1
        self.args = input_arguments

    def handle(self, seep_time) -> SinglePinCommonResult:
        if self.args.is_test_mode is False:
            from RPi import GPIO
            # Die Tonhoehe kann mit Variation der Wartezeit (sleep) veraendert werden
            # while true ist noetig, da sonst kein Ton ausgegeben wird.
            while True:
                GPIO.output(self.speaker, True)
                sleep(0.0005)
                GPIO.output(self.speaker, False)
                sleep(0.0005)
        return SinglePinCommonResult(True)

    def open(self):
        if self.args.is_test_mode is True:
            from RPi import GPIO
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.speaker, GPIO.OUT)

    def close(self):
        if self.args.is_test_mode is True:
            from RPi import GPIO
            GPIO.cleanup(self.speaker)

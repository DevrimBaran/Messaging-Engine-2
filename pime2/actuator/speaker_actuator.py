# pylint: disable=import-outside-toplevel
import logging

from pime2.actuator.actuator import SinglePinActuator, ActuatorType
from pime2.common.operator import SinglePinOperatorArguments
from time import sleep


class Speaker(SinglePinActuator):
    """
    A simple speaker
    """

    def __init__(self, input_arguments: SinglePinOperatorArguments):
        super().__init__(ActuatorType.SPEAKER, input_arguments)
        self.speaker = input_arguments.input_pin_1
        self.args = input_arguments
        self.speaker_on = False

    def activate(self, sleep_time: float):
        self.speaker_on = True
        if self.args.is_test_mode is False:
            from RPi import GPIO
            logging.info("Speaker is on")
            # Die Tonhoehe kann mit Variation der Wartezeit (sleep) veraendert werden
            # while true ist noetig, da sonst kein Ton ausgegeben wird.
            while True:
                GPIO.output(self.speaker, True)
                sleep(sleep_time)
                GPIO.output(self.speaker, False)
                sleep(sleep_time)

    def open(self):
        if self.args.is_test_mode is True:
            from RPi import GPIO
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.speaker, GPIO.OUT)
            logging.info("")

    def close(self):
        if self.args.is_test_mode is True:
            from RPi import GPIO
            GPIO.cleanup(self.speaker)
        self.speaker = False

    def is_speaker_on(self):
        return self.speaker_on

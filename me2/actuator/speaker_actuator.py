# pylint: disable=import-outside-toplevel
import logging
import time

from me2.actuator.actuator import SingleGpioActuator, ActuatorType
from me2.common.operator import SingleGpioOperatorArguments


class Speaker(SingleGpioActuator):
    """
    A simple speaker actuator.
    input_arguments provide a property is_test_mode.
    """

    def __init__(self, name: str, input_arguments: SingleGpioOperatorArguments):
        super().__init__(name, ActuatorType.SPEAKER, input_arguments)
        self.speaker = input_arguments.input_gpio_1
        self.args = input_arguments

    def handle(self, *input_args: str):
        # input variables all have default values, if there's an input the value will be set according to this order:
        # First input is the duration for how long the speaker is active, the second and third one are for the pitch
        # of the speaker.
        if len(input_args) == 0:
            sleep_time_for_pitch = 0.02
            sleep_time2_for_pitch = sleep_time_for_pitch
            duration = 2.0
        elif len(input_args) == 1:
            duration = float(input_args[0])
            sleep_time_for_pitch = 0.02
            sleep_time2_for_pitch = sleep_time_for_pitch
        elif len(input_args) == 2:
            # When no duration will be set but pitch will be set.
            if input_args[0] == "":
                duration = 2.0
            else:
                duration = float(input_args[0])
            sleep_time_for_pitch = float(input_args[1])
            sleep_time2_for_pitch = sleep_time_for_pitch
        elif len(input_args) == 3:
            # When no duration will be set but pitch will be set.
            if input_args[0] == "":
                duration = 2.0
            else:
                duration = float(input_args[0])
            sleep_time_for_pitch = float(input_args[1])
            sleep_time2_for_pitch = float(input_args[2])
        else:
            raise RuntimeError("Too many input arguments")
        start_time = time.time()
        elapsed_time = 0
        if self.args.is_test_mode is False:
            from RPi import GPIO
            logging.info("Speaker is on")
            # The pitch can be changed with variations of the sleep_time (time.sleep).
            # while true is necessary, otherwise there will be no sound.
            start_time = time.time()
            elapsed_time = 0
            while elapsed_time <= duration:
                GPIO.output(self.speaker, True)
                time.sleep(sleep_time_for_pitch)
                GPIO.output(self.speaker, False)
                time.sleep(sleep_time2_for_pitch)
                elapsed_time = time.time() - start_time
        else:
            logging.info("Dummy Speaker is on")
            while elapsed_time <= duration:
                elapsed_time = time.time() - start_time
        logging.info("Speaker is off")

    def open(self):
        if self.args.is_test_mode is False:
            from RPi import GPIO
            logging.info("Setting GPIO for speaker")
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.speaker, GPIO.OUT)

    def close(self):
        if self.args.is_test_mode is False:
            from RPi import GPIO
            logging.info("Cleaning GPIO ports for speaker")
            GPIO.cleanup(self.speaker)

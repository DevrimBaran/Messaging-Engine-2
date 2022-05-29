# pylint: disable=import-outside-toplevel
import logging
import time

from pime2.actuator.actuator import SingleGpioActuator, ActuatorType
from pime2.common.operator import SingleGpioOperatorArguments


class Speaker(SingleGpioActuator):
    """
    A simple speaker actuator.
    input_arguments provide a property is_test_mode.
    """

    def __init__(self, name: str, input_arguments: SingleGpioOperatorArguments):
        super().__init__(name, ActuatorType.SPEAKER, input_arguments)
        self.speaker = input_arguments.input_gpio_1
        self.args = input_arguments
        self.speaker_on = False

    def activate(self, input_arg_one: str, *input_args: str):
        sleep_time = float(input_arg_one)
        if len(input_args) == 0:
            sleep_time2 = sleep_time
            duration = 2.0
        elif len(input_args) == 1:
            sleep_time2 = float(input_args[0])
            duration = 2.0
        elif len(input_args) == 2:
            if input_args[0] == "":
                sleep_time2 = sleep_time
                duration = float(input_args[1])
            else:
                sleep_time2 = float(input_args[0])
                duration = float(input_args[1])
        else:
            raise RuntimeError("Too many input arguments")
        self.speaker_on = True
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
                time.sleep(sleep_time)
                GPIO.output(self.speaker, False)
                time.sleep(sleep_time2)
                elapsed_time = time.time() - start_time
        else:
            logging.info("Dummy Speaker is on")
            while elapsed_time <= 2.0:
                elapsed_time = time.time() - start_time

    def open(self):
        if self.args.is_test_mode is False:
            from RPi import GPIO
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.speaker, GPIO.OUT)

    def close(self):
        if self.args.is_test_mode is False:
            from RPi import GPIO
            GPIO.cleanup(self.speaker)
        self.speaker = False
        logging.info("Speaker is off")

    def is_speaker_on(self):
        """
        Getter for the variable speaker_on.
        """
        return self.speaker_on

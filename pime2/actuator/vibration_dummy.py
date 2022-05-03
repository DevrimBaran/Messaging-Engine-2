import logging

from pime2.actuator.actuator import SinglePinActuator
from pime2.common.operator import SinglePinOperatorArguments


class Vibration(SinglePinActuator):
    """
    A simple vibration motor which vibrates
    """

    def __init__(self, input_arguments: SinglePinOperatorArguments):
        super().__init__(input_arguments)
        self.vibration = input_arguments.input_pin_1
        self.args = input_arguments

    def handle(self, trigger_args: any) -> bool:
        pass

    def open(self):
        # TODO: Will be done in Issue PIME-27 Anbindung der Aktuatoren über GPIO
        pass

    def close(self):
        # TODO: Will be done in Issue PIME-27 Anbindung der Aktuatoren über GPIO
        pass


def vibration_dummy(var_on):
    """
    vibration dummy
    """
    if var_on == 1:
        logging.info("Vibration motor is on")
        return True
    return False

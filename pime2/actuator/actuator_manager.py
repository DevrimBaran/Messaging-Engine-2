# pylint: disable=consider-using-enumerate
import logging
import sys

from pime2.config import MEConfiguration
from pime2.actuator.actuator import ActuatorType


class ActuatorManager:
    """
    Simple actuator manager to activate and close actuators
    """
    def __init__(self, config: MEConfiguration):
        try:
            self.actuators = config.available_actuators()
        except RuntimeError as config_error:
            logging.error("Problem with sensor configuration: '%s'", config_error)
            sys.exit(1)

    def open(self, actuator_type: ActuatorType):
        """
        Open actuators.

        :param actuator_type:
        """
        count = 0
        for i in range(len(self.actuators)):
            if self.actuators[i].actuator_type == actuator_type:
                self.actuators[i].open()
                count += 1
        logging.info("Started %d actuators", count)

    def trigger(self, actuator_type: ActuatorType, *actuator_input_args: str):
        """.
        Trigger actuators.

        :param actuator_type:
        :param actuator_input_args:
        """
        count = 0
        for i in range(len(self.actuators)):
            if self.actuators[i].actuator_type == actuator_type:
                self.actuators[i].handle(*actuator_input_args)
                count += 1
        logging.info("Triggered %d actuators", count)

    def close(self, actuator_type: ActuatorType):
        """
        Close defined actuators

        :param actuator_type:
        """
        for i in range(len(self.actuators)):
            if self.actuators[i].actuator_type == actuator_type:
                self.actuators[i].close()

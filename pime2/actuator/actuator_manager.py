# pylint: disable=consider-using-enumerate
import logging
import sys

from pime2.config import MEConfiguration
from pime2.actuator.actuator import ActuatorType


class ActuatorManager:
    """
    Simple actuator manager to actvate and close actuators
    """
    def __init__(self, config: MEConfiguration):
        try:
            self.actuators = config.available_actuators()
        except RuntimeError as config_error:
            logging.error("Problem with sensor configuration: '%s'", config_error)
            sys.exit(1)

    def trigger(self, actuator_type: ActuatorType, actuator_input_one: str, actuator_input_two="-1",
                actuator_input_three="-1"):
        """
        start asyncio tasks and wait for them to complete.
        Should be called in main asyncio run().

        :param actuator_type:
        :param actuator_input_one:
        :param actuator_input_two:
        :param actuator_input_three:
        """
        count = 0
        for i in range(len(self.actuators)):
            if self.actuators[i].actuator_type == actuator_type:
                self.actuators[i].open()
                self.actuators[i].activate(actuator_input_one, actuator_input_two, actuator_input_three)
                count += 1
        logging.info("Started %d actuators", count)

    def close(self, actuator_type: ActuatorType):
        """
        Close defined actuators

        :param actuator_type:
        """
        for i in range(len(self.actuators)):
            if self.actuators[i].actuator_type == actuator_type:
                self.actuators[i].close()

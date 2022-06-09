# pylint: disable=consider-using-enumerate,keyword-arg-before-vararg
import logging
from typing import List

from pime2.config import get_me_conf
from pime2.actuator.actuator import ActuatorType


class ActuatorManager:
    """
    Simple actuator manager to activate and close actuators
    """

    def __init__(self):
        self.actuators = get_me_conf().available_actuators

    def open(self, actuator_type: ActuatorType):
        """
        Open actuators.

        :param actuator_type:
        """
        count = 0
        is_executed = False
        for i in range(len(self.actuators)):
            if self.actuators[i].actuator_type == actuator_type:
                self.actuators[i].open()
                is_executed = True
                count += 1
        if is_executed:
            logging.info("Started %d actuators", count)
        else:
            logging.warning("Actuator %s is not available", actuator_type.name)

    def trigger(self, actuator_type: ActuatorType = None, *actuator_input_args: str,
                actuators_list: List[str] = None):
        """
        Trigger actuators.

        :param actuator_type:
        :param actuators_list:
        :param actuator_input_args:
        """
        count = 0
        if actuators_list is None:
            for actuator in range(len(self.actuators)):
                if self.actuators[actuator].actuator_type == actuator_type:
                    self.actuators[actuator].handle(*actuator_input_args)
                    count += 1
        else:
            for actuator in range(len(self.actuators)):
                for input_actuator in range(len(actuators_list)):
                    if self.actuators[actuator].name == actuators_list[input_actuator]:
                        self.actuators[actuator].handle(*actuator_input_args)
                        count += 1
        logging.info("Triggered %d actuators of type %s", count, actuator_type.name)

    def close(self, actuator_type: ActuatorType):
        """
        Close defined actuators

        :param actuator_type:
        """
        for i in range(len(self.actuators)):
            if self.actuators[i].actuator_type == actuator_type:
                self.actuators[i].close()

    def one_time_trigger(self, actuator_type: ActuatorType):
        """Helper method to execute an actuator one single time"""
        self.open(actuator_type)
        try:
            self.trigger(actuator_type)
        finally:
            self.close(actuator_type)

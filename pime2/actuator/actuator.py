from abc import ABC, abstractmethod
from enum import Enum
from typing import Tuple

from pime2.common.operator import Operator, SingleGpioOperatorArguments, DualGpioOperatorArguments


class ActuatorType(Enum):
    """
    Enum to declare which actuator types are supported.
    """
    LED = 1
    SPEAKER = 2


class Actuator(Operator, ABC):
    """
    Abstract class to represent an abstract sensor.
    You should never inherit directly from this class, use SinglePinSensor, DualPinSensor...
    """

    def __init__(self, actuator_type: ActuatorType, name: str = "unknown"):
        self.actuator_type = actuator_type
        self.name = name

    @abstractmethod
    def activate(self, input_arg_one: str, *input_args: str):
        """
        Activate actuators with at least one input argument.
        :param input_arg_one:
        :param input_args:
        :return: success state - if any
        """


class SingleGpioActuator(Actuator, ABC):
    """
    Abstract class to represent an abstract sensor.
    Each actuator implements this class.

    """

    def __init__(self, name: str, actuator_type: ActuatorType, input_arguments: SingleGpioOperatorArguments):
        super().__init__(actuator_type, name)
        self.args = input_arguments


class DualGpioActuator(Actuator, ABC):
    """
    Abstract class to represent an abstract sensor.
    Each actuator implements this class.

    """

    def __init__(self, name: str, actuator_type: ActuatorType, input_arguments: DualGpioOperatorArguments):
        super().__init__(actuator_type, name)
        self.args = input_arguments

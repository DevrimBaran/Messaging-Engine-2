from abc import abstractmethod, ABC
from enum import Enum


# TODO: this is not final or perfect
# TODO: "types" is a bad package name ;)
# TODO: add meaningful properties to these objects
# TODO implement type of sensor/actuator


class Operator(ABC):
    """
    Abstract technical representation of an operator, which is Sensor + Actuator
    """

    @abstractmethod
    def open(self):
        """
        Method to initialize (or test) a sensor during startup. Called only once(?).
        :return:
        """

    @abstractmethod
    def close(self):
        """
        Method to shut down an operator
        :return:
        """


class OperatorArguments(ABC):
    """
    Abstract class to represent operator-wide common properties, e.g. at least one GPIO pin.
    """

    def __init__(self, pin: int, is_test_mode: bool = False):
        self.input_pin = pin
        self.is_test_mode = is_test_mode
        pass


class SensorType(Enum):
    TEMPERATURE = 1
    BUTTON = 2
    LED = 3


class SensorReadOutput(ABC):
    """
    Abstract class to represent the output of a single sensor reading process.
    Properties are missing.
    """

    def __init__(self, value):
        self.value = value
        pass

    def __str__(self):
        return "{\"result\": \"%s\"}" % self.value


class Sensor(Operator, ABC):
    """
    Abstract class to represent an abstract sensor.
    Each sensor implements this class.

    """

    def __init__(self, input_arguments: OperatorArguments):
        self.args = input_arguments

    @abstractmethod
    def read(self) -> SensorReadOutput:
        """
        Read data from sensor and write ot to the output.
        Very time critical.

        :return:
        """


class Actuator(Operator, ABC):
    """
    Abstract class to represent an abstract sensor.
    Each actuator implements this class.

    """

    def __init__(self, input_arguments: OperatorArguments):
        self.args = input_arguments

    @abstractmethod
    def handle(self, trigger_args: any) -> bool:
        """
        Process current gpio state of a (single?) pin and control the actuator operation.
        TODO: input type is tbd

        :param trigger_args:
        :return: success state - if any
        """

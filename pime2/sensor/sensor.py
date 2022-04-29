from abc import abstractmethod, ABC
from enum import Enum
from pime2.gpio_sensor_actuator.operator import Operator, TwoPinOperatorArguments, SinglePinOperatorArguments
from pime2.gpio_sensor_actuator.read_output import SinglePinSensorReadOutput, TwoPinSensorReadOutput


class SensorType(Enum):
    """
    Enum to declare which type of sensor is used.
    """
    TEMPERATURE = 1
    BUTTON = 2
    # Hall sensors detect magnetic fields
    HALL = 3


class Sensor(Operator, ABC):
    """
    Abstract class to represent an abstract sensor.
    """
    def __init__(self, sensor_type):
        self.sensor_type = sensor_type


class TwoPinSensor(Sensor, ABC):
    """
    Abstract class to represent an abstract two output pin sensor.
    Each two pin sensor implements this class.
    """
    def __init__(self, sensor_type: SensorType, input_arguments: TwoPinOperatorArguments):
        super().__init__(sensor_type)
        self.args = input_arguments

    @abstractmethod
    def read(self) -> TwoPinSensorReadOutput:
        """
        Read data from sensor and write ot to the output.
        Very time critical.
        :return:
        """


class SinglePinSensor(Sensor, ABC):
    """
    Abstract class to represent an abstract single output pin sensor.
    Each single pin sensor implements this class.
    """
    def __init__(self, sensor_type: SensorType, input_arguments: SinglePinOperatorArguments):
        super().__init__(sensor_type)
        self.args = input_arguments

    @abstractmethod
    def read(self) -> SinglePinSensorReadOutput:
        """
        Read data from sensor and write ot to the output.
        Very time critical.
        :return:
        """

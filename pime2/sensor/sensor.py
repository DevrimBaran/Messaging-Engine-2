from abc import abstractmethod, ABC
from enum import Enum
from pime2.common.operator import Operator, DualPinOperatorArguments, SinglePinOperatorArguments
from pime2.common.read_output import SinglePinSensorReadOutput, DualPinSensorReadOutput


class SensorType(Enum):
    """
    Enum to declare which sensor types are supported.
    """
    TEMPERATURE = 1
    BUTTON = 2
    # Hall sensors detect magnetic fields
    HALL = 3


class Sensor(Operator, ABC):
    """
    Abstract class to represent an abstract sensor.
    You should never inherit directly from this class, use SinglePinSensor, DualPinSensor...
    """

    def __init__(self, sensor_type):
        self.sensor_type = sensor_type


class DualPinSensor(Sensor, ABC):
    """
    Abstract class to represent an abstract two output pin sensor.
    Each two pin sensor implements this class.
    """

    def __init__(self, sensor_type: SensorType, input_arguments: DualPinOperatorArguments):
        super().__init__(sensor_type)
        self.args = input_arguments

    @abstractmethod
    def read(self) -> DualPinSensorReadOutput:
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
        Read data from sensor and write ot to the output - a single time.
        Very time critical.
        :return:
        """
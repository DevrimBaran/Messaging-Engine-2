from abc import abstractmethod, ABC
from enum import Enum
from pime2.common.operator import Operator, DualGpioOperatorArguments, SingleGpioOperatorArguments
from pime2.common.read_output import DualGpioCommonResult, SingleGpioCommonResult


class SensorType(Enum):
    """
    Enum to declare which sensor types are supported.
    """
    TEMPERATURE = "TEMPERATURE"
    BUTTON = "BUTTON"
    # Hall sensors detect magnetic fields
    HALL = "HALL"


class Sensor(Operator, ABC):
    """
    Abstract class to represent an abstract sensor.
    You should never inherit directly from this class, use SingleGpioSensor, DualGpioSensor...
    """

    def __init__(self, sensor_type: SensorType, name: str = "unknown"):
        self.sensor_type = sensor_type
        self.name = name

    @abstractmethod
    def read(self) -> DualGpioCommonResult:
        """
        Read data from sensor and write ot to the output.
        Very time critical.
        :return:
        """


class DualGpioSensor(Sensor, ABC):
    """
    Abstract class to represent an abstract two output pin sensor.
    Each two pin sensor implements this class.
    """

    def __init__(self, name: str, sensor_type: SensorType, input_arguments: DualGpioOperatorArguments):
        super().__init__(sensor_type, name)
        self.args = input_arguments

    @abstractmethod
    def read(self) -> DualGpioCommonResult:
        """
        Read data from sensor and write ot to the output.
        Very time critical.
        :return:
        """


class SingleGpioSensor(Sensor, ABC):
    """
    Abstract class to represent an abstract single output pin sensor.
    Each single pin sensor implements this class.
    """

    def __init__(self, name: str, sensor_type: SensorType, input_arguments: SingleGpioOperatorArguments):
        super().__init__(sensor_type, name)
        self.args = input_arguments

    @abstractmethod
    def read(self) -> SingleGpioCommonResult:
        """
        Read data from sensor and write ot to the output.
        Very time critical.
        :return:
        """

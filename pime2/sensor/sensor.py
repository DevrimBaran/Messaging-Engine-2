from abc import abstractmethod, ABC
from enum import Enum


# TODO: this is not final or perfect
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


class SinglePinOperatorArguments(ABC):
    """
    Abstract class to represent operator-wide common properties, e.g. one GPIO pin.
    """

    def __init__(self, pin: int, is_test_mode: bool = False):
        self.input_pin = pin
        self.is_test_mode = is_test_mode


class TwoPinOperatorArguments(SinglePinOperatorArguments, ABC):
    """
    Abstract class to represent two pin operator-wide common properties, e.g. two GPIO pin.
    """

    def __init__(self, pin: int, pin_2: int, is_test_mode: bool = False):
        super().__init__(pin, is_test_mode)
        self.input_pin_2 = pin_2


class SensorType(Enum):
    TEMPERATURE = 1
    BUTTON = 2
    LED = 3


class SinglePinSensorReadOutput(ABC):
    """
    Abstract class to represent the output of a single sensor reading process.
    Properties are missing.
    """

    def __init__(self, result):
        self.result = result

    def __str__(self):
        return f"{{\"result\": \"{self.result}\"}}"


class TwoPinSensorReadOutput(ABC):

    def __init__(self, pin_1_result, pin_2_result):
        self.pin_1_result = pin_1_result
        self.pin_2_result = pin_2_result

    def __str__(self):
        return f"{{\"Result for pin 1\": \"{self.pin_1_result}\", \"Result for pin 2\": \"{self.pin_2_result}\" }}"


class Sensor(Operator, ABC):
    """
    Abstract class to represent an abstract sensor.
    Each sensor implements this class.

    """
    def __init__(self, sensor_type):
        self.sensor_type = sensor_type


class TwoPinSensor(Sensor, ABC):
    """
    Abstract class to represent an abstract two pin sensor.
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


class Actuator(Operator, ABC):
    """
    Abstract class to represent an abstract sensor.
    Each actuator implements this class.

    """

    def __init__(self, input_arguments: SinglePinOperatorArguments):
        self.args = input_arguments

    @abstractmethod
    def handle(self, trigger_args: any) -> bool:
        """
        Process current gpio state of a (single?) pin and control the actuator operation.
        TODO: input type is tbd

        :param trigger_args:
        :return: success state - if any
        """

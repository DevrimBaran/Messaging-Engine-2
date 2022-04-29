from abc import ABC, abstractmethod


class Operator(ABC):
    """
    Abstract technical representation of an gpio_sensor_actuator, which is Sensor + Actuator
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
        Method to shut down an gpio_sensor_actuator
        :return:
        """


class SinglePinOperatorArguments(ABC):
    """
    Abstract class to represent single input pin gpio_sensor_actuator-wide common properties, e.g. one GPIO pin.
    """

    def __init__(self, input_pin_1: int, is_test_mode: bool = False):
        self.input_pin_1 = input_pin_1
        self.is_test_mode = is_test_mode


class DualPinOperatorArguments(SinglePinOperatorArguments, ABC):
    """
    Abstract class to represent two input pin gpio_sensor_actuator-wide common properties, e.g. two GPIO pins.
    """

    def __init__(self, input_pin_1: int, input_pin_2: int, is_test_mode: bool = False):
        super().__init__(input_pin_1, is_test_mode)
        self.input_pin_2 = input_pin_2

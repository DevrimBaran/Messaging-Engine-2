# pylint: disable=too-few-public-methods
from abc import ABC, abstractmethod


class Operator(ABC):
    """
    Abstract technical representation of a common, which is Sensor + Actuator
    """

    @abstractmethod
    def open(self):
        """
        Method to initialize (or test) a common during startup. Called only once or after .close().
        :return:
        """

    @abstractmethod
    def close(self):
        """
        Method to shut down a common
        :return:
        """


class SingleGpioOperatorArguments(ABC):
    """
    Abstract class to represent single input gpio common-wide common properties, e.g. one GPIO pin.
    """

    def __init__(self, input_gpio_1: int, is_test_mode: bool = False):
        self.input_gpio_1 = input_gpio_1
        self.is_test_mode = is_test_mode


class DualGpioOperatorArguments(SingleGpioOperatorArguments, ABC):
    """
    Abstract class to represent two input gpio common-wide common properties, e.g. two GPIO pins.
    """

    def __init__(self, input_gpio_1: int, input_gpio_2: int, is_test_mode: bool = False):
        super().__init__(input_gpio_1, is_test_mode)
        self.input_gpio_2 = input_gpio_2

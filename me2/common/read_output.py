from abc import ABC


class SingleGpioCommonResult(ABC):
    """
    Abstract class to represent the output of a single output pin sensor reading process.
    """

    def __init__(self, result):
        self.result = result


class DualGpioCommonResult(ABC):
    """
    Abstract class to represent the output of a two output input pin sensor reading process.
    """

    def __init__(self, gpio_1_result, gpio_2_result):
        self.gpio_1_result = gpio_1_result
        self.gpio_2_result = gpio_2_result

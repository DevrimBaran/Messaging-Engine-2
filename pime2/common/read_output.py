from abc import ABC


class SinglePinCommonResult(ABC):
    """
    Abstract class to represent the output of a single output pin sensor reading process.
    """

    def __init__(self, result):
        self.result = result


class DualPinCommonResult(ABC):
    """
    Abstract class to represent the output of a two output input pin sensor reading process.
    """

    def __init__(self, pin_1_result, pin_2_result):
        self.pin_1_result = pin_1_result
        self.pin_2_result = pin_2_result

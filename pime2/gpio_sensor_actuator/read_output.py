from abc import ABC


class SinglePinSensorReadOutput(ABC):
    """
    Abstract class to represent the output of a single output pin sensor reading process.
    """
    def __init__(self, result):
        self.result = result

    def __str__(self):
        return f"{{\"result\": \"{self.result}\"}}"


class TwoPinSensorReadOutput(ABC):
    """
    Abstract class to represent the output of a two output input pin sensor reading process.
    """
    def __init__(self, pin_1_result, pin_2_result):
        self.pin_1_result = pin_1_result
        self.pin_2_result = pin_2_result

    def __str__(self):
        return f"{{\"Result for input 1\": \"{self.pin_1_result}\", \"Result for input 2\": \"{self.pin_2_result}\" }}"
# pylint: disable=import-outside-toplevel
import logging
import random
import typing

from pime2.sensor.sensor import SingleGpioSensor, SensorType, SingleGpioOperatorArguments
from pime2.common.read_output import SingleGpioCommonResult


class TemperatureSensorResult(SingleGpioCommonResult):
    """
    Simple type for a temperature reading
    """

    def __init__(self, result: typing.Optional[float]):
        super().__init__(result)


class TemperatureSensor(SingleGpioSensor):
    """
    A simple temperature sensor.
    input_arguments provide a property is_test_mode.
    """

    def __init__(self, name: str, input_arguments: SingleGpioOperatorArguments):
        super().__init__(name, SensorType.TEMPERATURE, input_arguments)
        self.sensor_gpio: int = input_arguments.input_gpio_1
        self.sensor = None
        self.args = input_arguments

    def read(self) -> TemperatureSensorResult:
        if self.args.is_test_mode is False:
            # start sensor listening
            temperature = -100
            if self.sensor is None:
                logging.error(
                    "Sensor object is None and seems not to be opened. Severe problem with the usage of "
                    "temperature sensor.")
                return TemperatureSensorResult(float(temperature))
            try:
                temp_c = self.sensor.temperature
                if temp_c is not None:
                    # pylint: disable=consider-using-f-string
                    logging.info("Temp:{0:0.1f}°C".format(temp_c))
                    temperature = temp_c
            except RuntimeError as error:
                if len(error.args) > 0:
                    logging.error("Problem reading temperature sensor: %s", error.args[0])
                    temperature = error.args[0]
                else:
                    logging.error("Unknown problem reading temperature sensor")
            if isinstance(temperature, float):
                return TemperatureSensorResult(float(temperature))
            # log any error the sensor returns and return None as result.
            logging.error(temperature)
            return TemperatureSensorResult(None)
        # Temperature sensor dummy logic
        random_temperature = float(random.randint(-50, 50) + random.random())
        logging.info("Temp:%.1f°C", random_temperature)
        return TemperatureSensorResult(random_temperature)

    def open(self):
        if self.args.is_test_mode is False:
            # pylint: disable=unused-import
            import board
            import adafruit_dht
            # Set input GPIO for Sensor and set pulseio to False so that the GPIO still can be used after
            # shutdown of program
            self.sensor = adafruit_dht.DHT22(board.D12, use_pulseio=False)

    def close(self):
        # Not necessary since use_pulseio is set to False
        pass

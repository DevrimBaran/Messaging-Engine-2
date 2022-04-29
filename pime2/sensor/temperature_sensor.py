# pylint: disable=consider-using-f-string
import logging
import random

from pime2.sensor.sensor import SinglePinSensor, SensorType, SinglePinOperatorArguments
from pime2.gpio_sensor_actuator.read_output import SinglePinSensorReadOutput


class TemperatureSensor(SinglePinSensor):
    """
    A simple temperature sensor
    """
    def __init__(self, sensor_type: SensorType, input_arguments: SinglePinOperatorArguments):
        super().__init__(sensor_type.TEMPERATURE, input_arguments)
        self.sensor = input_arguments.input_pin_1
        self.args = input_arguments

    def read(self) -> SinglePinSensorReadOutput:
        if self.args.is_test_mode is False:
            import board
            import adafruit_dht
            while True:
                try:
                    temp_c = self.sensor.temperature
                    if temp_c is not None:
                        logging.info("Temp:{0:0.1f}°C".format(temp_c))
                        temperature = temp_c
                        break
                    logging.error("Failed to get reading. Try again!")
                    continue
                except RuntimeError as error:
                    logging.error(error.args[0])
                    temperature = error.args[0]
                    break
            return SinglePinSensorReadOutput(temperature)
        random_temperature = random.randint(-50, 50)
        # pylint would not accept following log
        logging.info("Temp: " + str(random_temperature))
        return SinglePinSensorReadOutput(random_temperature)

    def open(self):
        if self.args.is_test_mode is True:
            import board
            import adafruit_dht
            # Set input pin for Sensor and set pulseio to False so that pin still can be used after shutdown of program
            self.sensor = adafruit_dht.DHT22(board.D12, use_pulseio=False)

    def close(self):
        # Not necassary since use_puseio is set to False
        pass

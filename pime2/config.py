import ipaddress
import logging
import os
import pathlib
import typing
from typing import List

import yaml

from pime2.actuator.actuator import Actuator, ActuatorType
from pime2.actuator.led_actuator import Led
from pime2.actuator.speaker_actuator import Speaker
from pime2.common.operator import DualGpioOperatorArguments, SingleGpioOperatorArguments
from pime2.sensor.button_sensor import ButtonSensor
from pime2.sensor.hall_sensor import HallSensor
from pime2.sensor.sensor import Sensor, SensorType
from pime2.sensor.temperature_sensor import TemperatureSensor

CONFIG_FILE = "me.yaml"


class MEConfiguration:
    """
    This class represents the app's configuration yaml file.
    """

    def __init__(self, config_yaml) -> None:
        if config_yaml is None:
            raise RuntimeError("Invalid empty configuration given.")

        required_elements = [
            "instance_id",
            "loglevel",
            "host",
            "port",
            "read_interval",
        ]
        for i in required_elements:
            if i not in config_yaml or config_yaml[i] is None:
                raise RuntimeError(f"Missing '{i}' in configuration.")

        self.instance_id = str(config_yaml['instance_id']).strip()
        self.loglevel = str(config_yaml['loglevel']).strip()
        self.host = str(config_yaml['host']).strip()
        self.port = int(str(config_yaml['port']).strip())
        self.read_interval = float(str(config_yaml['read_interval']).strip())

        if len(self.instance_id) == 0:
            raise RuntimeError("Empty 'instance_id' not allowed in configuration.")
        if len(self.loglevel) == 0:
            raise RuntimeError("Empty 'loglevel' not allowed in configuration.")
        if len(self.host) == 0:
            raise RuntimeError("Empty 'host' not allowed in configuration.")
        if self.port <= 0 or self.port >= pow(2, 16) or config_yaml['port'] is None:
            raise RuntimeError("Invalid 'port' not allowed in configuration.")
        if self.read_interval < 0.3 or self.read_interval > 300:
            raise RuntimeError("Invalid 'read_interval' not allowed in configuration.")

        # host needs to be a valid ip
        try:
            ipaddress.ip_address(self.host)
        except ValueError as ex:
            raise RuntimeError("Invalid ip given in 'host' field") from ex

        if 'is_debug' in config_yaml:
            self.is_debug = bool(config_yaml['is_debug'])
        else:
            self.is_debug = False

        if 'is_neighbor_discovery_enabled' in config_yaml:
            self.is_neighbor_discovery_enabled = bool(config_yaml['is_neighbor_discovery_enabled'])
        else:
            self.is_neighbor_discovery_enabled = False

        self.sensors = []
        self.actuators = []

        if 'sensors' in config_yaml and config_yaml['sensors'] is not None:
            for sensor_config in config_yaml['sensors']:
                self.sensors.append(OperatorConfiguration(sensor_config))

        if 'actuators' in config_yaml and config_yaml['actuators'] is not None:
            for actuator_config in config_yaml['actuators']:
                self.actuators.append(OperatorConfiguration(actuator_config))

    def available_sensors(self) -> List[Sensor]:
        """
        Method to get sensor objects defined in the app's configuration.
        Could raise a RuntimeError, if there is something wrongly configured.
        :return:
        """
        return load_sensors(self)

    def available_actuators(self) -> List[Actuator]:
        """
        Method to get actuator objects defined in the app's configuration.
        Could raise a RuntimeError, if there is something wrongly configured.
        :return:
        """
        return load_actuators(self)


class OperatorConfiguration:
    """
    Internal class to represent an operator (sensor/actuator) in the configuration yaml file.
    """

    def __init__(self, operator_object):
        if 'name' not in operator_object or 'type' not in operator_object or 'gpio1' not in operator_object:
            raise RuntimeError("Missing at least one mandatory operator property: name, type, gpio1")

        if operator_object['name'] is None or operator_object['type'] is None or operator_object['gpio1'] is None:
            raise RuntimeError("Missing at least one mandatory operator property value of: name, type, gpio1")

        if not isinstance(operator_object['gpio1'], int):
            raise RuntimeError("Invalid non integer given for gpio1.")
        if 'gpio2' in operator_object and operator_object['gpio2'] is not None and not isinstance(
                operator_object['gpio2'], int):
            raise RuntimeError("Invalid non integer given for gpio gpio2.")

        self.name = str(operator_object['name']).strip()
        self.type = str(operator_object['type']).strip()
        self.gpio1 = int(operator_object['gpio1'])
        self.is_test_mode = False
        if 'is_test_mode' in operator_object and operator_object['is_test_mode'] is True:
            self.is_test_mode = True

        if 'gpio2' in operator_object:
            self.gpio2 = int(operator_object['gpio2'])
        else:
            self.gpio2 = 0
        self.original = operator_object


ME_CONF: MEConfiguration


def load_app_config(config_file_path: str) -> typing.Optional[MEConfiguration]:
    """
    internal method to load the yml file and insert it into an instance of MEConfiguration class
    :return:
    """
    # pylint: disable=global-statement
    global ME_CONF
    try:
        default_config_file = os.path.join(pathlib.Path(__file__).parent.parent.resolve(), config_file_path)
        if os.path.exists(default_config_file):
            with open(default_config_file, "r", encoding="utf-8") as config_file:
                app_config_raw = yaml.safe_load(config_file)
                ME_CONF = MEConfiguration(app_config_raw)
                return ME_CONF
    except RuntimeError as ex:
        raise RuntimeError(f"Cannot find configuration file '{config_file_path}' or cannot load it. {ex}") from ex
    return None


def get_me_conf() -> MEConfiguration:
    """
    This method provides the app's properties

    :return:
    """
    return ME_CONF


def load_sensors(config: MEConfiguration) -> List[Sensor]:
    """
    This method maps the textual configuration of available sensors to internal classes.
    This is called during application bootstrap process. If there are problem with the configuration the user
    provided, this method should raise RuntimeErrors with detailed error information for the user.
    :param config:
    :return:
    """
    active_sensors: List[Sensor] = []
    for sensor in config.sensors:
        # basic validation
        if len(str(sensor.name).strip()) == 0:
            raise RuntimeError("Empty name of a sensor detected")
        if sensor.gpio1 == 0 or len(str(sensor.gpio1).strip()) == 0:
            raise RuntimeError("Empty or invalid port detected in property 'gpio1'")

        sensor_type = str(sensor.type).upper()
        if sensor.is_test_mode:
            logging.info("Using test mode for sensor of type '%s' and name '%s'", sensor_type, sensor.name)

        if sensor_type == SensorType.BUTTON.name:
            if sensor.gpio2 == 0 or len(str(sensor.gpio2).strip()) == 0:
                raise RuntimeError("Empty or invalid port detected in property 'gpio2'")

            active_sensors.append(
                ButtonSensor(sensor.name, DualGpioOperatorArguments(sensor.gpio1, sensor.gpio2, sensor.is_test_mode)))
        elif sensor_type == SensorType.HALL.name:
            active_sensors.append(
                HallSensor(sensor.name, SingleGpioOperatorArguments(sensor.gpio1, sensor.is_test_mode)))
        elif sensor_type == SensorType.TEMPERATURE.name:
            active_sensors.append(
                TemperatureSensor(sensor.name, SingleGpioOperatorArguments(sensor.gpio1, sensor.is_test_mode)))
        else:
            raise RuntimeError("Unknown sensor type '{]'", sensor_type)
    return active_sensors


def load_actuators(config: MEConfiguration) -> List[Actuator]:
    """
    This method maps the textual configuration of available actuators to internal classes.
    This is called during application bootstrap process. If there are problem with the configuration the user
    provided, this method should raise RuntimeErrors with detailed error information for the user.
    :param config:
    :return:
    """
    active_actuators: List[Actuator] = []
    for actuator in config.actuators:
        # basic validation
        if len(str(actuator.name).strip()) == 0:
            raise RuntimeError("Empty name of a actuator detected")
        if actuator.gpio1 == 0 or len(str(actuator.gpio1).strip()) == 0:
            raise RuntimeError("Empty or invalid port detected in property 'gpio1'")

        actuator_type = str(actuator.type).upper()
        if actuator.is_test_mode:
            logging.info("Using test mode for actuator of type '%s' and name '%s'", actuator_type, actuator.name)

        if actuator_type == ActuatorType.LED.name:
            if actuator.gpio2 == 0 or len(str(actuator.gpio2).strip()) == 0:
                raise RuntimeError("Empty or invalid port detected in property 'gpio2'")

            active_actuators.append(
                Led(actuator.name, DualGpioOperatorArguments(actuator.gpio1, actuator.gpio2, actuator.is_test_mode)))
        elif actuator_type == ActuatorType.SPEAKER.name:
            active_actuators.append(
                Speaker(actuator.name, SingleGpioOperatorArguments(actuator.gpio1, actuator.is_test_mode)))
        else:
            raise RuntimeError("Unknown sensor type '{]'", actuator_type)
    return active_actuators

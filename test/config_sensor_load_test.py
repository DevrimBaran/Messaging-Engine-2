import unittest

import pime2.config
import pime2.sensor.sensor


class TestAppConfigurationSensorLoad(unittest.TestCase):

    def test_sensor_load_button(self):
        is_exceptional = False
        try:
            config = pime2.config.load_app_config("./test/fixtures/me_valid_with_operators_button.yaml")
        except RuntimeError:
            is_exceptional = True
        self.assertFalse(is_exceptional)
        self.assertIsNotNone(config)
        sensors = pime2.config.load_sensors(config)
        self.assertEqual(1, len(sensors))
        self.assertEqual("Testsensor", sensors[0].name)
        self.assertEqual(pime2.sensor.sensor.SensorType.BUTTON, sensors[0].sensor_type)

    def test_sensor_load_hall(self):
        is_exceptional = False
        try:
            config = pime2.config.load_app_config("./test/fixtures/me_valid_with_operators_hall.yaml")
        except RuntimeError:
            is_exceptional = True
        self.assertFalse(is_exceptional)
        self.assertIsNotNone(config)
        sensors = pime2.config.load_sensors(config)
        self.assertEqual(1, len(sensors))
        self.assertEqual("Testsensor2", sensors[0].name)
        self.assertEqual(pime2.sensor.sensor.SensorType.HALL, sensors[0].sensor_type)

    def test_sensor_load_hall(self):
        is_exceptional = False
        try:
            config = pime2.config.load_app_config("./test/fixtures/me_valid_with_operators_temperature.yaml")
        except RuntimeError:
            is_exceptional = True
        self.assertFalse(is_exceptional)
        self.assertIsNotNone(config)
        sensors = pime2.config.load_sensors(config)
        self.assertEqual(1, len(sensors))
        self.assertEqual("TemperatureSensor", sensors[0].name)
        self.assertEqual(pime2.sensor.sensor.SensorType.TEMPERATURE, sensors[0].sensor_type)


if __name__ == '__main__':
    unittest.main()

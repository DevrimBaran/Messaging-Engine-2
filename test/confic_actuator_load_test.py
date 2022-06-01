import unittest

import pime2.config
import pime2.actuator.actuator


class TestAppConfigurationActuatorLoad(unittest.TestCase):

    def test_actuator_load_speaker(self):
        is_exceptional = False
        try:
            config = pime2.config.load_app_config("./test/fixtures/me_valid_actuator_speaker.yaml")
        except RuntimeError:
            is_exceptional = True
        self.assertFalse(is_exceptional)
        self.assertIsNotNone(config)
        actuators = pime2.config.load_actuators(config)
        self.assertEqual(1, len(actuators))
        self.assertEqual("Testactuator", actuators[0].name)
        self.assertEqual(pime2.actuator.actuator.ActuatorType.SPEAKER, actuators[0].actuator_type)

    def test_actuator_load_led(self):
        is_exceptional = False
        try:
            config = pime2.config.load_app_config("./test/fixtures/me_valid_actuator_led.yaml")
        except RuntimeError:
            is_exceptional = True
        self.assertFalse(is_exceptional)
        self.assertIsNotNone(config)
        actuators = pime2.config.load_actuators(config)
        self.assertEqual(1, len(actuators))
        self.assertEqual("Testactuator", actuators[0].name)
        self.assertEqual(pime2.actuator.actuator.ActuatorType.LED, actuators[0].actuator_type)


if __name__ == '__main__':
    unittest.main()

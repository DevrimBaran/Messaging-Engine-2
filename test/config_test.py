import unittest

import pime2.config


class TestAppConfiguration(unittest.TestCase):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        # these paths need to be relative to the repository root
        self.valid_config_files = [
            './test/fixtures/me_valid_1.yaml',
            './test/fixtures/me_valid_2.yaml',
            './test/fixtures/me_valid_3.yaml',
            './test/fixtures/me_valid_4.yaml',
            './test/fixtures/me_valid_5.yaml',
        ]
        self.valid_config_files_with_operators = [
            './test/fixtures/me_valid_with_operators_button.yaml',
            './test/fixtures/me_valid_with_operators_button2.yaml',
        ]
        self.invalid_config_files = [
            './test/fixtures/me_invalid_1.yaml',
            './test/fixtures/me_invalid_2.yaml',
            './test/fixtures/me_invalid_3.yaml',
            './test/fixtures/me_invalid_4.yaml',
            './test/fixtures/me_invalid_5.yaml',
            './test/fixtures/me_invalid_6.yaml',
            './test/fixtures/me_invalid_7.yaml',
            './test/fixtures/me_invalid_8.yaml',
            './test/fixtures/me_invalid_9.yaml',
            './test/fixtures/me_invalid_10.yaml',
            './test/fixtures/me_invalid_11.yaml',
            './test/fixtures/me_invalid_12.yaml',
            './test/fixtures/me_invalid_13.yaml',
            './test/fixtures/me_invalid_14.yaml',
            './test/fixtures/me_invalid_15.yaml',
            './test/fixtures/me_invalid_16.yaml',
            './test/fixtures/me_invalid_17.yaml',
        ]

    def test_valid_configuration_works(self):
        for i in self.valid_config_files:
            is_exceptional = False
            try:
                config = pime2.config.load_app_config(i)
            except RuntimeError:
                is_exceptional = True
            self.assertFalse(is_exceptional)
            self.assertIsNotNone(config)
            self.assertEqual("12345678", config.instance_id)
            self.assertEqual("DEBUG", config.loglevel)
            self.assertEqual(False, config.is_debug)
            self.assertEqual("127.0.0.1", config.host)
            self.assertEqual(5683, config.port)

            self.assertEqual(0, len(config.sensors))
            self.assertEqual(0, len(config.actuators))

    def test_valid_configuration_works_with_operators(self):
        for i in self.valid_config_files_with_operators:
            is_exceptional = False
            try:
                config = pime2.config.load_app_config(i)
            except RuntimeError:
                is_exceptional = True
            self.assertFalse(is_exceptional)
            self.assertIsNotNone(config)
            self.assertEqual("12345678", config.instance_id)
            self.assertEqual("DEBUG", config.loglevel)
            self.assertEqual(False, config.is_debug)
            self.assertEqual("127.0.0.1", config.host)
            self.assertEqual(5683, config.port)

            self.assertEqual(1, len(config.sensors))
            self.assertEqual(0, len(config.actuators))

    def test_invalid_configuration_does_not_work(self):
        for i in self.invalid_config_files:
            is_exceptional = False
            try:
                pime2.config.load_app_config(i)
            except RuntimeError:
                is_exceptional = True
            self.assertTrue(is_exceptional)

    def test_operator_configuration(self):
        invalid_operators = [
            {},
            {"name": ""},
            {"name": "", "is_test_mode": False},
            {"name": "", "gpio1": ""},
            {"name": "", "type": ""},
            {"type": ""},
            {"type": "", "gpio1": ""},
            {"gpio1": ""}
        ]

        for i in invalid_operators:
            is_exceptional = False
            try:
                configuration = pime2.config.OperatorConfiguration(i)
            except RuntimeError:
                is_exceptional = True
            self.assertTrue(is_exceptional)


if __name__ == '__main__':
    unittest.main()

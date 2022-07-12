import unittest
from pime2.flow.filter_flow import filter_executer

class TestCEPFlow(unittest.TestCase):


    def test_simple_operators(self):
        self.assertTrue(filter_executer(expression="6 + 4 == 10", variables={}, payload={}))
        self.assertTrue(filter_executer(expression="0 - 53 == -53", variables={}, payload={}))
        self.assertTrue(filter_executer(expression="3 * 18 == 54", variables={}, payload={}))
        self.assertTrue(filter_executer(expression="45 / 9 == 5", variables={}, payload={}))
        self.assertTrue(filter_executer(expression="7.5 + 3.22 == 10.72", variables={}, payload={}))

        self.assertFalse(filter_executer(expression="6 + 4 == 18", variables={}, payload={}))
        self.assertFalse(filter_executer(expression="0 - 53 == 53", variables={}, payload={}))
        self.assertFalse(filter_executer(expression="3 * 18 == 23", variables={}, payload={}))
        self.assertFalse(filter_executer(expression="45 / 9 == 3", variables={}, payload={}))
        self.assertFalse(filter_executer(expression="7.5 - 3.22 == 10.72", variables={}, payload={}))

    def test_comparison_operators(self):
        self.assertTrue(filter_executer(expression="7 == 7", variables={}, payload={}))
        self.assertTrue(filter_executer(expression="7 != 9", variables={}, payload={}))
        self.assertTrue(filter_executer(expression="0 < 10", variables={}, payload={}))
        self.assertTrue(filter_executer(expression="10 > -8", variables={}, payload={}))
        self.assertTrue(filter_executer(expression="9 <= 10", variables={}, payload={}))
        self.assertTrue(filter_executer(expression="12 >= 11", variables={}, payload={}))

        self.assertFalse(filter_executer(expression="7 != 7", variables={}, payload={}))
        self.assertFalse(filter_executer(expression="7 == 9", variables={}, payload={}))
        self.assertFalse(filter_executer(expression="0 > 10", variables={}, payload={}))
        self.assertFalse(filter_executer(expression="10 < -8", variables={}, payload={}))
        self.assertFalse(filter_executer(expression="13 <= 10", variables={}, payload={}))
        self.assertFalse(filter_executer(expression="12 >= 14", variables={}, payload={}))

    def test_boolean_operators(self):
        self.assertTrue(filter_executer(expression="7 == 7 and 3 < 5", variables={}, payload={}))
        self.assertTrue(filter_executer(expression="4 != 3 or 4 == 4", variables={}, payload={}))
        self.assertTrue(filter_executer(expression="8 >= 4 and 7 + 3 == 12 or 8 + 2 == 10 ", variables={}, payload={}))
        self.assertTrue(filter_executer(expression="True ", variables={}, payload={}))
        self.assertTrue(filter_executer(expression="true", variables={}, payload={}))
        self.assertTrue(filter_executer(expression="true or false", variables={}, payload={}))
        
        self.assertFalse(filter_executer(expression="7 != 7 and 3 < 5", variables={}, payload={}))
        self.assertFalse(filter_executer(expression="4 == 3 or 4 < 2", variables={}, payload={}))
        self.assertFalse(filter_executer(expression="8 == 4 and 7 + 3 == 12 or 8 + 2 == 12 ", variables={}, payload={}))
        self.assertFalse(filter_executer(expression="False", variables={}, payload={}))
        self.assertFalse(filter_executer(expression="false", variables={}, payload={}))
        self.assertFalse(filter_executer(expression="false and true", variables={}, payload={}))

    def test_expression_with_variables(self):
        self.assertTrue(filter_executer(expression="x + 4 == 10", variables={"x": 6}, payload={}))
        self.assertTrue(filter_executer(expression="x + y == 28", variables={"x": 0, "y": 28}, payload={}))
        self.assertTrue(filter_executer(expression="y - x == -28", variables={"x": 28, "y": 0}, payload={}))
        self.assertTrue(filter_executer(expression="0 > x and y + 3 > 4 or 50 - x == 40", variables={"x": 10, "y": 5}, payload={}))
        self.assertFalse(filter_executer(expression="y - x != -24", variables={"x": 24, "y": 0}, payload={}))
        self.assertFalse(filter_executer(expression="0 > y and 5 + 3 > 4 and x - 10 == 40", variables={"x": 3, "y": 5}, payload={}))
        self.assertFalse(filter_executer(expression="0.0 > 10 and x + 3 < y and 50 - 10 == 40", variables={"x": 7, "y": 9}, payload={}))

    def test_expression_with_variables_and_payload(self):
        self.assertTrue(filter_executer(expression="x + 7 == 25", variables={"x": "result"}, payload='{"result": 18}'))
        self.assertTrue(filter_executer(expression="x + 4 == 28.7", variables={"x": "gpio_1_result"}, payload='{"gpio_1_result": 24.7}'))
        self.assertTrue(filter_executer(expression="x + y == 48", variables={"x": "gpio_1_result", "y": "gpio_2_result"}, payload='{"gpio_1_result": 0, "gpio_2_result": 48}'))
        self.assertTrue(filter_executer(expression="y - x == -24", variables={"x": 24, "y": 0}, payload='{"u": 3, "y": 2}'))

    def test_complex_expression(self):
        self.assertTrue(filter_executer(expression="(x > 20 and x > y) or (y > 20 and x == 24 + 4)", variables={"x": "gpio_1_result", "y": "gpio_2_result"}, payload='{"gpio_1_result": 23, "gpio_2_result": 11}'))
        self.assertFalse(filter_executer(expression="(x > 20 and x < y) or (y > 20 and x == 24 + 4)", variables={"x": "gpio_1_result", "y": "gpio_2_result"}, payload='{"gpio_1_result": 23, "gpio_2_result": 11}'))
        self.assertFalse(filter_executer(expression="(x > 20 and x < y) or (y > 20 and x == 24 + 4)", variables={"x": "gpio_1_result", "y": "gpio_2_result"}, payload='{"gpio_1_result": 23, "gpio_2_result": 11}'))

    def test_invalid_input(self):
        self.assertFalse(filter_executer(expression="6 + 4 == 10-", variables={}, payload={}))
        self.assertFalse(filter_executer(expression="0 - 53 =!= -53", variables={}, payload={}))
        self.assertFalse(filter_executer(expression="x + 7 == 25", variables={"x": "reult"}, payload='{"result": 18}'))
        self.assertFalse(filter_executer(expression="x + 4 == 28.7", variables={"x": "gpio_3_result"}, payload='{"gpio_1_result": 24.7}'))


if __name__ == '__main__':
    unittest.main()
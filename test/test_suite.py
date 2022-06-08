import unittest
import test.flow_test as flow_test
import test.config_test as config_test
import test.config_sensor_load_test as config_sensor_load_test
import test.config_actuator_load_test as config_actuator_load_test
import test.database_test as database_test
import test.flow_repository_test as flow_repository_test
import test.flow_mapper_test as flow_mapper_test
import test.flow_operation_manager_test as flow_operation_manager_test
import test.flow_service_test as flow_service_test
import test.node_mapper_test as node_mapper_test
import test.node_repository_test as node_repository_test


class TestSuite(unittest.TestCase):
    """
        Gather all the tests from this module in a test suite.
    """


test_suite = unittest.TestSuite()
loader = unittest.TestLoader()
test_suite.addTest(loader.loadTestsFromModule(flow_test))
test_suite.addTest(loader.loadTestsFromModule(config_test))
test_suite.addTest(loader.loadTestsFromModule(config_sensor_load_test))
test_suite.addTest(loader.loadTestsFromModule(config_actuator_load_test))
test_suite.addTest(loader.loadTestsFromModule(database_test))
test_suite.addTest(loader.loadTestsFromModule(flow_mapper_test))
test_suite.addTest(loader.loadTestsFromModule(flow_service_test))
test_suite.addTest(loader.loadTestsFromModule(flow_repository_test))
test_suite.addTest(loader.loadTestsFromModule(flow_operation_manager_test))
test_suite.addTest(loader.loadTestsFromModule(node_mapper_test))
test_suite.addTest(loader.loadTestsFromModule(node_repository_test))

runner = unittest.TextTestRunner(verbosity=3)
runner.run(test_suite)

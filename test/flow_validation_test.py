import os
import unittest

from pime2 import database
from pime2.config import load_app_config
from pime2.flow import flow_validation_service
from pime2.entity import FlowOperationEntity, FlowEntity
from pime2.repository.node_repository import NodeRepository


class MyTestCase(unittest.TestCase):
    node_repo: NodeRepository = None
    connection = None

    @classmethod
    def setUp(cls):
        if os.path.exists("testDatabase.db"):
            database.disconnect(cls.connection)
            os.remove("testDatabase.db")
        load_app_config("me.yaml")
        cls.connection = database.create_connection("testDatabase.db")
        cls.node_repo = NodeRepository(cls.connection)
        database.create_default_tables(cls.connection)

    def test_valid_flow_validation(self):
        test_name = "op_name"
        test_name2 = "op_name2"
        test_name3 = "op_name3"
        test_op_name = "sensor_temperature"
        flow_ops = [FlowOperationEntity(test_name, test_op_name, None, "actuator_led", "*"),
                    FlowOperationEntity(test_name2, None, "log", None, "*"),
                    FlowOperationEntity(test_name3, None, "cep_intercept", "actuator_speaker", "*")]
        flow = FlowEntity("test_flow", flow_ops)
        self.assertEqual(flow_validation_service.is_flow_valid(flow), (True,))

    def test_invalid_flow_validation(self):
        test_name = "op_name"
        test_name2 = "op_name2"
        test_name3 = "op_name3"
        test_op_name = "sensor_temperature"
        flow_ops = [FlowOperationEntity(test_name, test_op_name, None, "actuator_led", "*"),
                    FlowOperationEntity(test_name2, None, None, None, "*"),
                    FlowOperationEntity(test_name3, None, "cep_intercept", "actuator_speaker_test", "*")]
        flow = FlowEntity("test_flow", flow_ops)
        self.assertEqual((False, "Wrong input for output!"), flow_validation_service.is_flow_valid(flow))
        flow_ops2 = [FlowOperationEntity(test_name, test_op_name, None, "actuator_led", "*"),
                     FlowOperationEntity(test_name2, None, "log", None, "*"),
                     FlowOperationEntity(test_name3, None, "cep_intercept_test", "actuator_speaker", "*")]
        flow2 = FlowEntity("test_flow", flow_ops2)
        self.assertEqual((False, "Wrong input for process!"), flow_validation_service.is_flow_valid(flow2))
        flow_ops3 = [FlowOperationEntity(test_name, "test_op_name", None, "actuator_led", "*"),
                     FlowOperationEntity(test_name2, None, "log", None, "*"),
                     FlowOperationEntity(test_name3, None, "cep_intercept", "actuator_speaker", "*")]
        flow3 = FlowEntity("test_flow", flow_ops3)
        self.assertEqual((False, "Wrong input operation!"), flow_validation_service.is_flow_valid(flow3))
        flow_ops4 = []
        flow4 = FlowEntity("test_flow", flow_ops4)
        self.assertEqual((False, "Got flow without operations!"), flow_validation_service.is_flow_valid(flow4), )
        flow_ops5 = [FlowOperationEntity(test_name, "test_op_name", None, "actuator_led", "*")]
        flow5 = FlowEntity("test_flow", flow_ops5)
        self.assertEqual((False, "Got flow with too less operations!"), flow_validation_service.is_flow_valid(flow5))
        flow_ops6 = [FlowOperationEntity(test_name, test_op_name, None, "actuator_led", "*"),
                     FlowOperationEntity(test_name2, None, "log", None, "*"),
                     FlowOperationEntity(test_name3, test_op_name, "cep_intercept", "actuator_speaker", "*")]
        flow6 = FlowEntity("test_flow", flow_ops6)
        self.assertEqual((False, "Only one input is allowed in a flow!"), flow_validation_service.is_flow_valid(flow6))
        flow_ops7 = [FlowOperationEntity(test_name, test_op_name, None, "actuator_led", "*"),
                     FlowOperationEntity(test_name2, None, "log", None, "*"),
                     FlowOperationEntity(test_name3, None, "cep_intercept_test", "actuator_speaker")]
        flow7 = FlowEntity("test_flow", flow_ops7)
        self.assertEqual((False, "Wrong input for process!"), flow_validation_service.is_flow_valid(flow7))
        flow_ops8 = [FlowOperationEntity(test_name, test_op_name, None, None, "*"),
                     FlowOperationEntity(test_name2, None, "log", None, "*"),
                     FlowOperationEntity(test_name3, None, "cep_intercept", None)]
        flow8 = FlowEntity("test_flow", flow_ops8)
        self.assertEqual((False, "No output defined!"), flow_validation_service.is_flow_valid(flow8))
        flow_ops9 = [FlowOperationEntity(test_name, None, None, "actuator_led", "*"),
                     FlowOperationEntity(test_name2, None, "log", None, "*"),
                     FlowOperationEntity(test_name3, None, "cep_intercept", "actuator_speaker")]
        flow9 = FlowEntity("test_flow", flow_ops9)
        self.assertEqual((False, "No input defined!"), flow_validation_service.is_flow_valid(flow9))
        flow_ops10 = [FlowOperationEntity(test_name, test_op_name, None, "actuator_led", "*"),
                      FlowOperationEntity(test_name2, None, "log", None, "*"),
                      FlowOperationEntity(test_name3, None, "cep_intercept", "actuator_speaker", "test")]
        flow10 = FlowEntity("test_flow", flow_ops10)
        self.assertEqual((False, "Can not execute node step execution!"), flow_validation_service.is_flow_valid(flow10))
        flow_ops11 = [FlowOperationEntity(test_name, test_op_name, None, "actuator_led", "*"),
                      FlowOperationEntity(test_name, None, "log", None, "*"),
                      FlowOperationEntity(test_name3, None, "cep_intercept", "actuator_speaker")]
        flow11 = FlowEntity("test_flow", flow_ops11)
        self.assertEqual((False, "Operation names need to be unique per flow!"),
                         flow_validation_service.is_flow_valid(flow11))

    @classmethod
    def tearDownClass(cls):
        database.disconnect(cls.connection)
        os.remove("testDatabase.db")


if __name__ == '__main__':
    unittest.main()

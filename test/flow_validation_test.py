import os
import unittest

from pime2 import NAME_REGEX, database
from pime2.config import load_app_config
from pime2.database import create_connection
from pime2.entity import FlowOperationEntity, FlowEntity
from pime2.flow.flow_validation import is_flow_valid, is_flow_step_executable
from pime2.repository.node_repository import NodeRepository
from pime2.service.node_service import NodeService


class FlowValidationTest(unittest.TestCase):
    connection: None = create_connection("testDatabase.db")

    @classmethod
    def setUp(cls):
        if os.path.exists("testDatabase.db"):
            database.disconnect(cls.connection)
            os.remove("testDatabase.db")
        load_app_config("me.yaml")
        cls.connection = database.create_connection("testDatabase.db")
        cls.node_repo = NodeRepository(cls.connection)
        database.create_default_tables(cls.connection, NodeService())

    @classmethod
    def tearDownClass(cls) -> None:
        database.disconnect(cls.connection)
        os.remove("testDatabase.db")

    def test_valid_flow_validation(self):
        self.node_repo.delete_all()

        database.create_default_tables(self.connection, NodeService())

        sql_insert_testdata = """INSERT INTO nodes (name, ip, port)
                                            VALUES 
                                                ('node1', "10.10.10.1", 5683),
                                                ('node2', "10.10.10.2", 5683),
                                                ('node3', "10.10.10.3", 5683);"""

        cursor = self.connection.cursor()
        cursor.execute(sql_insert_testdata)
        self.connection.commit()

        cursor.close()

        flow_ops = [FlowOperationEntity("op_name", "sensor_temperature", None, None, "*"),
                    FlowOperationEntity("op_name2", None, None, "actuator_led", "node1, node2"),
                    FlowOperationEntity("op_name3", None, "cep_intercept", None, "node1")]
        flow = FlowEntity("test_flow", flow_ops)
        self.assertEqual(True, is_flow_valid(flow)[0])
        self.assertEqual(True, is_flow_step_executable(flow, "op_name3", NodeService()))

    def test_invalid_flow_validation(self):
        test_name = "op_name"
        test_name2 = "op_name2"
        test_name3 = "op_name3"
        test_op_name = "sensor_temperature"
        test_op_name2 = "sensor_button"
        test_op_name3 = "sensor_hall"
        test_process_op = "log"
        test_process_op2 = "cep_intercept"
        test_output_op = "actuator_led"
        test_output_op2 = "actuator_speaker"
        node_service = NodeService()
        flow_ops = [FlowOperationEntity(test_name, test_op_name, None, None, "*"),
                    FlowOperationEntity(test_name2, None, test_process_op, None, "*"),
                    FlowOperationEntity(test_name3, None, None, "actuator_speaker_test", "*")]
        flow = FlowEntity("test_flow", flow_ops)
        self.assertEqual((False, "Wrong input for output-operation!"), is_flow_valid(flow))
        flow_ops2 = [FlowOperationEntity(test_name, test_op_name2, None, None, "*"),
                     FlowOperationEntity(test_name2, None, None, test_output_op, "*"),
                     FlowOperationEntity(test_name3, None, "cep_intercept_test", None, "*")]
        flow2 = FlowEntity("test_flow", flow_ops2)
        self.assertEqual((False, "Wrong input for process-operation!"), is_flow_valid(flow2))
        flow_ops3 = [FlowOperationEntity(test_name, "test_op_name", None, None, "*"),
                     FlowOperationEntity(test_name2, None, test_process_op, None, "*"),
                     FlowOperationEntity(test_name3, None, None, test_output_op2, "*")]
        flow3 = FlowEntity("test_flow", flow_ops3)
        self.assertEqual((False, "Wrong input operation!"), is_flow_valid(flow3))
        flow_ops4 = []
        flow4 = FlowEntity("test_flow", flow_ops4)
        self.assertEqual((False, "Got flow without operations!"), is_flow_valid(flow4), )
        flow_ops5 = [FlowOperationEntity(test_name, test_op_name, None, None, "*")]
        flow5 = FlowEntity("test_flow", flow_ops5)
        self.assertEqual((False, "Got flow with too less operations!"), is_flow_valid(flow5))
        flow_ops6 = [FlowOperationEntity(test_name, test_op_name, None, None, "*"),
                     FlowOperationEntity(test_name2, None, None, test_output_op, "*"),
                     FlowOperationEntity(test_name3, test_op_name, None, None, "*")]
        flow6 = FlowEntity("test_flow", flow_ops6)
        self.assertEqual((False, "Only one input is allowed in a flow!"), is_flow_valid(flow6))
        flow_ops7 = [FlowOperationEntity(test_name, test_op_name3, None, None, "*"),
                     FlowOperationEntity(test_name2, None, test_process_op, None, "*"),
                     FlowOperationEntity(test_name3, None, "cep_intercept_test", None)]
        flow7 = FlowEntity("test_flow", flow_ops7)
        self.assertEqual((False, "Wrong input for process-operation!"), is_flow_valid(flow7))
        flow_ops8 = [FlowOperationEntity(test_name, test_op_name, None, None, "*"),
                     FlowOperationEntity(test_name2, None, test_process_op, None, "*"),
                     FlowOperationEntity(test_name3, None, test_process_op2, None)]
        flow8 = FlowEntity("test_flow", flow_ops8)
        self.assertEqual((False, "No output defined!"), is_flow_valid(flow8))
        flow_ops9 = [FlowOperationEntity(test_name, None, test_process_op, None, "*"),
                     FlowOperationEntity(test_name2, None, None, test_output_op, "*"),
                     FlowOperationEntity(test_name3, None, test_process_op2, None)]
        flow9 = FlowEntity("test_flow", flow_ops9)
        self.assertEqual((False, "No input defined!"), is_flow_valid(flow9))
        flow_ops10 = [FlowOperationEntity(test_name, test_op_name, None, None, "*"),
                      FlowOperationEntity(test_name2, None, test_process_op, None, "*"),
                      FlowOperationEntity(test_name3, None, None, test_output_op2, "test")]
        flow10 = FlowEntity("test_flow", flow_ops10)
        self.assertEqual(False, is_flow_step_executable(flow10, test_name3, node_service))
        flow_ops11 = [FlowOperationEntity(test_name, test_op_name, None, None, "*"),
                      FlowOperationEntity(test_name, None, test_process_op, None, "*"),
                      FlowOperationEntity(test_name3, None, None, test_output_op2)]
        flow11 = FlowEntity("test_flow", flow_ops11)
        self.assertEqual((False, "Operation names need to be unique per flow!"),
                         is_flow_valid(flow11))
        flow_ops12 = [FlowOperationEntity(test_name, test_op_name, None, None, "*"),
                      FlowOperationEntity("@", None, test_process_op, None, "*"),
                      FlowOperationEntity(test_name3, None, None, test_output_op2)]
        flow12 = FlowEntity("test_flow", flow_ops12)
        self.assertEqual((False, f"Operation Name should match following regex: {NAME_REGEX}"),
                         is_flow_valid(flow12))
        flow_ops13 = [FlowOperationEntity(test_name, test_op_name, None, test_output_op, "*"),
                      FlowOperationEntity(test_name2, None, test_process_op, None, "*"),
                      FlowOperationEntity(test_name3, None, test_process_op2, test_output_op2)]
        flow13 = FlowEntity("@", flow_ops13)
        self.assertEqual((False, f"Flow Name should match following regex: {NAME_REGEX}"),
                         is_flow_valid(flow13))
        flow_ops14 = [FlowOperationEntity(test_name, test_op_name, None, test_output_op, "*"),
                      FlowOperationEntity(test_name2, None, test_process_op, None, "*"),
                      FlowOperationEntity(test_name3, None, test_process_op2, None)]
        flow14 = FlowEntity("test_flow", flow_ops14)
        self.assertEqual((False, "Only one of the following types are allowed per flow: 'input', 'process', 'output'!"),
                         is_flow_valid(flow14))

    def test_is_flow_executable(self):
        node_service = NodeService()
        # TODO: this code can be uncommented once the skill-feature works
        # # wrong input
        # flow = FlowEntity("test_flow", [
        #     FlowOperationEntity("op_name1", "sensor_temp", None, None),
        #     FlowOperationEntity("op_name2", None, "log", None),
        #     FlowOperationEntity("op_name3", None, None, "exit"),
        # ])
        # self.assertFalse(is_flow_executable(flow, node_service))
        #
        # # wrong output
        # flow = FlowEntity("test_flow", [
        #     FlowOperationEntity("op_name1", "sensor_temperature", None, None),
        #     FlowOperationEntity("op_name2", None, "log", None),
        #     FlowOperationEntity("op_name3", None, None, "TEST"),
        # ])
        # self.assertFalse(is_flow_executable(flow, node_service))

        # test exit is allowed
        flow = FlowEntity("test_flow", [
            FlowOperationEntity("op_name1", "sensor_temperature", None, None),
            FlowOperationEntity("op_name2", None, "log", None),
            FlowOperationEntity("op_name3", None, None, "exit"),
        ])
        self.assertTrue(is_flow_step_executable(flow, "op_name3", node_service))


if __name__ == '__main__':
    unittest.main()

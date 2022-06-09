import os
import unittest

from pime2 import database, NAME_REGEX
from pime2.entity import FlowOperationEntity, FlowEntity
from pime2.flow.flow_validation import is_flow_valid


class FlowValidationTest(unittest.TestCase):
    def test_valid_flow_validation(self):
        flow_ops = [FlowOperationEntity("op_name", "sensor_temperature", None, None, "*"),
                    FlowOperationEntity("op_name2", None, None, "actuator_led", "node1, node2"),
                    FlowOperationEntity("op_name3", None, "cep_intercept", None, "node1")]
        flow = FlowEntity("test_flow", flow_ops)
        self.assertEqual(True, is_flow_valid(flow))

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
        flow_ops = [FlowOperationEntity(test_name, test_op_name, None, None, "*"),
                    FlowOperationEntity(test_name2, None, test_process_op, None, "*"),
                    FlowOperationEntity(test_name3, None, None, "actuator_speaker_test", "*")]
        flow = FlowEntity("test_flow", flow_ops)
        self.assertEqual((False, "Wrong input for output!"), is_flow_valid(flow))
        flow_ops2 = [FlowOperationEntity(test_name, test_op_name2, None, None, "*"),
                     FlowOperationEntity(test_name2, None, None, test_output_op, "*"),
                     FlowOperationEntity(test_name3, None, "cep_intercept_test", None, "*")]
        flow2 = FlowEntity("test_flow", flow_ops2)
        self.assertEqual((False, "Wrong input for process!"), is_flow_valid(flow2))
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
        self.assertEqual((False, "Wrong input for process!"), is_flow_valid(flow7))
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


if __name__ == '__main__':
    unittest.main()

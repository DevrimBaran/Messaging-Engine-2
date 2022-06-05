import unittest

from pime2.flow import flow_validation_service
from pime2.entity import FlowMessageEntity, FlowOperationEntity, FlowEntity


class MyTestCase(unittest.TestCase):
    def test_valid_flow_validation(self):
        test_name = "op_name"
        test_name2 = "op_name2"
        test_op_name = "sensor_temperature"
        flow_ops = [FlowOperationEntity(test_name, test_op_name, None, "actuator_led", "*"),
                    FlowOperationEntity(test_name2, None, "log", None, "*"),
                    FlowOperationEntity(test_name, None, "cep_intercept", "actuator_speaker", "*")]
        flow = FlowEntity("test_flow", flow_ops)
        self.assertEqual(flow_validation_service.is_flow_valid(flow), (True, []))

    def test_invalid_flow_validation(self):
        test_name = "op_name"
        test_name2 = "op_name2"
        test_op_name = "sensor_temperature"
        flow_ops = [FlowOperationEntity(test_name, test_op_name, None, "actuator_led", "*"),
                    FlowOperationEntity(test_name2, None, None, None, "*"),
                    FlowOperationEntity(test_name, None, "cep_intercept", "actuator_speaker_test", "*")]
        flow = FlowEntity("test_flow", flow_ops)
        self.assertEqual(flow_validation_service.is_flow_valid(flow),
                         (False, ["Wrong input for output!"]))
        flow_ops2 = [FlowOperationEntity(test_name, test_op_name, None, "actuator_led", "*"),
                     FlowOperationEntity(test_name2, None, "log", None, "*"),
                     FlowOperationEntity(test_name, None, "cep_intercept_test", "actuator_speaker", "*")]
        flow2 = FlowEntity("test_flow", flow_ops2)
        self.assertEqual(flow_validation_service.is_flow_valid(flow2),
                         (False, ["Wrong input for process!"]))
        flow_ops3 = [FlowOperationEntity(test_name, "test_op_name", None, "actuator_led", "*"),
                     FlowOperationEntity(test_name2, None, "log", None, "*"),
                     FlowOperationEntity(test_name, None, "cep_intercept", "actuator_speaker", "*")]
        flow3 = FlowEntity("test_flow", flow_ops3)
        self.assertEqual(flow_validation_service.is_flow_valid(flow3),
                         (False,
                          ["Wrong input operation!"]))
        flow_ops4 = []
        flow4 = FlowEntity("test_flow", flow_ops4)
        self.assertEqual(flow_validation_service.is_flow_valid(flow4),
                         (False,
                          ["Got flow without operations!"]))
        flow_ops5 = [FlowOperationEntity(test_name, "test_op_name", None, "actuator_led", "*")]
        flow5 = FlowEntity("test_flow", flow_ops5)
        self.assertEqual(flow_validation_service.is_flow_valid(flow5),
                         (False,
                          ["Got flow with too less operations!"]))
        flow_ops6 = [FlowOperationEntity(test_name, test_op_name, None, "actuator_led", "*"),
                     FlowOperationEntity(test_name2, None, "log", None, "*"),
                     FlowOperationEntity(test_name, test_op_name, "cep_intercept", "actuator_speaker", "*")]
        flow6 = FlowEntity("test_flow", flow_ops6)
        self.assertEqual(flow_validation_service.is_flow_valid(flow6),
                         (False,
                          ["Only one input is allowed in a flow!"]))
        flow_ops7 = [FlowOperationEntity(test_name, test_op_name, None, "actuator_led", "*"),
                     FlowOperationEntity(test_name2, None, "log", None, "*"),
                     FlowOperationEntity(test_name, None, "cep_intercept_test", "actuator_speaker")]
        flow7 = FlowEntity("test_flow", flow_ops7)
        self.assertEqual(flow_validation_service.is_flow_valid(flow7),
                         (False,
                          ["Wrong input for process!"]))
        flow_ops8 = [FlowOperationEntity(test_name, test_op_name, None, None, "*"),
                     FlowOperationEntity(test_name2, None, "log", None, "*"),
                     FlowOperationEntity(test_name, None, "cep_intercept", None)]
        flow8 = FlowEntity("test_flow", flow_ops8)
        self.assertEqual(flow_validation_service.is_flow_valid(flow8),
                         (False,
                          ["No output defined!"]))
        flow_ops9 = [FlowOperationEntity(test_name, None, None, "actuator_led", "*"),
                     FlowOperationEntity(test_name2, None, "log", None, "*"),
                     FlowOperationEntity(test_name, None, "cep_intercept", "actuator_speaker")]
        flow9 = FlowEntity("test_flow", flow_ops9)
        self.assertEqual(flow_validation_service.is_flow_valid(flow9),
                         (False,
                          ["No input defined!"]))


if __name__ == '__main__':
    unittest.main()

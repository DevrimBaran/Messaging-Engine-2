import unittest
import uuid
from datetime import datetime

from pime2.entity import FlowMessageEntity, FlowOperationEntity, FlowEntity


class TestAppConfiguration(unittest.TestCase):

    def test_flow_model_works(self):
        test_name = "op_name"
        test_name2 = "op_name2"
        test_op_name = "sensor_read_temperature"
        flow_ops = [FlowOperationEntity(test_name, test_op_name, None, None, "*"),
                    FlowOperationEntity(test_name2, None, "log", None, "*")]
        flow = FlowEntity("test_flow", flow_ops)
        self.assertEqual(2, len(flow_ops))
        self.assertEqual(test_name, flow.ops[0].name)
        self.assertEqual(test_op_name, flow.ops[0].input)
        self.assertIsNone(flow.ops[0].output)
        self.assertIsNone(flow.ops[0].process)
        self.assertEqual("*", flow.ops[0].where)
        self.assertEqual(test_name2, flow.ops[1].name)
        self.assertIsNone(flow.ops[1].input)
        self.assertEqual("log", flow.ops[1].process)
        self.assertIsNone(flow.ops[1].output)


if __name__ == '__main__':
    unittest.main()

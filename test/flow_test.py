import unittest
import uuid
from datetime import datetime

from pime2.entity import FlowMessageEntity, FlowOperationEntity, FlowEntity


class TestAppConfiguration(unittest.TestCase):

    def test_flow_model_works(self):
        flow_ops = [FlowOperationEntity("op_name", "sensor_read_temperature", None, None, "*"),
                    FlowOperationEntity("op_name2", None, "log", None, "*")]
        flow = FlowEntity("test_flow", flow_ops)
        self.assertEqual(2, len(flow_ops))
        self.assertIsNotNone(flow)

    def test_flow_message_model_works(self):
        fm = FlowMessageEntity(uuid.uuid4().hex, "flow_name", datetime.now(), datetime.now(), None, "log", "", 1, [])
        self.assertIsNotNone(fm)

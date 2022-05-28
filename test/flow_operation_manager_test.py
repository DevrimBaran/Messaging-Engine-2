import datetime
import unittest
import uuid

from pime2.entity import FlowEntity, FlowOperationEntity, FlowMessageEntity
from pime2.flow import FlowOperationManager


class FlowOperationManagerTest(unittest.TestCase):

    def test_is_last_step(self):
        fm = FlowOperationManager()

        for f in [self.simple_test_flow(), self.simple_test_flow2(), self.simple_test_flow3()]:
            self.assertFalse(fm.is_last_step(f, ""))
            self.assertFalse(fm.is_last_step(f, " "))

            self.assertFalse(fm.is_last_step(f, "first_step"))

            if len(f.ops) > 2:
                self.assertFalse(fm.is_last_step(f, "second_step"))

            self.assertTrue(fm.is_last_step(f, "last_step"))
            # case-insensitive
            self.assertTrue(fm.is_last_step(f, "LAST_step"))
            self.assertTrue(fm.is_last_step(f, "LAST_STeP"))
            self.assertFalse(fm.is_last_step(f, "LAST_step123"))
            self.assertFalse(fm.is_last_step(f, "LAST_step123   "))
            self.assertFalse(fm.is_last_step(f, "    LAST_step123"))

    def test_second_step(self):
        fm = FlowOperationManager()

        for f in [
            self.simple_test_flow(),
            self.simple_test_flow2(),
            self.simple_test_flow3(),
        ]:
            if len(f.ops) > 2:
                self.assertEquals("second_step", fm.detect_second_step(f))
            else:
                self.assertEquals("last_step", fm.detect_second_step(f))

    def test_current_step(self):
        fm = FlowOperationManager()
        now = datetime.datetime.now()

        for f in [
            self.simple_test_flow(),
            self.simple_test_flow2(),
            self.simple_test_flow3(),
        ]:
            message = FlowMessageEntity(uuid.uuid4().hex, "test_flow1", now, now, None, "last_step", "", 1, [])
            self.assertEquals("last_step", fm.detect_current_step(self.simple_test_flow(), message))

        message = FlowMessageEntity(uuid.uuid4().hex, "test_flow1", now, now, None, "second_step", "", 1, [])
        self.assertEquals("second_step", fm.detect_current_step(self.simple_test_flow(), message))

    def simple_test_flow(self):
        return FlowEntity("test_flow1", [
            FlowOperationEntity("first_step", "sensor_temperature", None, None),
            FlowOperationEntity("second_step", None, "log", None),
            FlowOperationEntity("last_step", None, None, "exit"),
        ])

    def simple_test_flow2(self):
        return FlowEntity("test_flow2", [
            FlowOperationEntity("first_step", "sensor_temperature", None, None),
            FlowOperationEntity("second_step", None, "log", None),
            FlowOperationEntity("third_step", None, "log2", None),
            FlowOperationEntity("last_step", None, None, "exit"),
        ])

    def simple_test_flow3(self):
        return FlowEntity("test_flow3", [
            FlowOperationEntity("first_step", "sensor_temperature", None, None),
            FlowOperationEntity("last_step", None, None, "exit"),
        ])


if __name__ == '__main__':
    unittest.main()

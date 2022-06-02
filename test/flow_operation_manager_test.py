import datetime
import unittest
import uuid

from pime2.entity import FlowEntity, FlowOperationEntity, FlowMessageEntity, NodeEntity
from pime2.flow import FlowOperationManager


class FlowOperationManagerTest(unittest.TestCase):

    def test_is_last_step(self):
        fm = FlowOperationManager()

        for f in [self.simple_test_flow1(), self.simple_test_flow2(), self.simple_test_flow3()]:
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
            self.simple_test_flow1(),
            self.simple_test_flow2(),
            self.simple_test_flow3(),
        ]:
            if len(f.ops) > 2:
                self.assertEqual("second_step", fm.detect_second_step(f))
            else:
                self.assertEqual("last_step", fm.detect_second_step(f))

    def test_current_step(self):
        fm = FlowOperationManager()
        now = datetime.datetime.now()

        for f in [
            self.simple_test_flow1(),
            self.simple_test_flow2(),
        ]:
            message = FlowMessageEntity(uuid.uuid4().hex, f.name, now, now, None, "last_step", "", 1, [])
            self.assertEqual("last_step", fm.detect_current_step(f, message))

            message = FlowMessageEntity(uuid.uuid4().hex, f.name, now, now, None, "second_step", "", 1, [])
            self.assertEqual("second_step", fm.detect_current_step(f, message))

            # remove required info and result should be null
            message = FlowMessageEntity(uuid.uuid4().hex, f.name, now, now, None, "", "", 1, [])
            self.assertIsNone(fm.detect_current_step(f, message))
            message = FlowMessageEntity(uuid.uuid4().hex, f.name, now, now, None, "unknown_step", "", 1, [])
            self.assertIsNone(fm.detect_current_step(f, message))

    def test_next_step(self):
        fm = FlowOperationManager()
        now = datetime.datetime.now()

        for f in [
            self.simple_test_flow1(),
            self.simple_test_flow2(),
        ]:
            message = FlowMessageEntity(uuid.uuid4().hex, f.name, now, now, "first_step", "", "", 1, [])
            self.assertEqual("second_step", fm.detect_next_step(f, message))
            message = FlowMessageEntity(uuid.uuid4().hex, f.name, now, now, "first_step", "last_step", "", 1, [])
            self.assertEqual("second_step", fm.detect_next_step(f, message))
            message = FlowMessageEntity(uuid.uuid4().hex, f.name, now, now, "first_step", "not_important", "", 1, [])
            self.assertEqual("second_step", fm.detect_next_step(f, message))

    def test_nodes_of_step(self):
        fm = FlowOperationManager()
        nodes = [
            NodeEntity("instance1", "127.0.0.1", 5683),
            NodeEntity("instance2", "127.0.0.2", 5683),
            NodeEntity("instance3", "127.0.0.3", 5683),
        ]
        # test "*"
        self.assertEqual(nodes, fm.detect_nodes_of_step(self.simple_test_flow1(), "first_step", nodes))
        self.assertEqual(nodes, fm.detect_nodes_of_step(self.simple_test_flow1(), "second_step", nodes))
        self.assertEqual(nodes, fm.detect_nodes_of_step(self.simple_test_flow1(), "last_step", nodes))

        # test single instance selection
        test_flow = self.simple_test_flow1()
        test_flow.ops[0].where = "instance1"
        test_flow.ops[1].where = "instance1"
        test_flow.ops[2].where = "instance1"
        self.assertEqual([nodes[0]], fm.detect_nodes_of_step(test_flow, "first_step", nodes))
        self.assertEqual([nodes[0]], fm.detect_nodes_of_step(test_flow, "second_step", nodes))
        self.assertEqual([nodes[0]], fm.detect_nodes_of_step(test_flow, "last_step", nodes))

        test_flow = self.simple_test_flow1()
        test_flow.ops[0].where = "instance1"
        test_flow.ops[1].where = "instance2"
        test_flow.ops[2].where = "instance3"
        self.assertEqual([nodes[0]], fm.detect_nodes_of_step(test_flow, "first_step", nodes))
        self.assertEqual([nodes[1]], fm.detect_nodes_of_step(test_flow, "second_step", nodes))
        self.assertEqual([nodes[2]], fm.detect_nodes_of_step(test_flow, "last_step", nodes))

        # check if no node is available
        test_flow = self.simple_test_flow1()
        test_flow.ops[0].where = "instance1"
        test_flow.ops[1].where = "instanceXY"
        test_flow.ops[2].where = "instance3"
        self.assertEqual([nodes[0]], fm.detect_nodes_of_step(test_flow, "first_step", nodes))
        self.assertEqual([], fm.detect_nodes_of_step(test_flow, "second_step", nodes))
        self.assertEqual([nodes[2]], fm.detect_nodes_of_step(test_flow, "last_step", nodes))

        # test single instance and wildcard mixed
        test_flow = self.simple_test_flow1()
        test_flow.ops[0].where = "*"
        test_flow.ops[1].where = "instance2"
        test_flow.ops[2].where = "*"
        self.assertEqual(nodes, fm.detect_nodes_of_step(test_flow, "first_step", nodes))
        self.assertEqual([nodes[1]], fm.detect_nodes_of_step(test_flow, "second_step", nodes))
        self.assertEqual(nodes, fm.detect_nodes_of_step(test_flow, "last_step", nodes))

        # test multiple instances
        test_flow = self.simple_test_flow1()
        test_flow.ops[0].where = "*"
        test_flow.ops[1].where = "instance1,instance2"
        test_flow.ops[2].where = "*"
        self.assertEqual(nodes, fm.detect_nodes_of_step(test_flow, "first_step", nodes))
        self.assertEqual(nodes[:2], fm.detect_nodes_of_step(test_flow, "second_step", nodes))
        self.assertEqual(nodes, fm.detect_nodes_of_step(test_flow, "last_step", nodes))

        test_flow = self.simple_test_flow1()
        test_flow.ops[0].where = "instance1,instance2  "
        test_flow.ops[1].where = "instance1, instance2"
        test_flow.ops[2].where = "instance1,instance2,"
        self.assertEqual(nodes[:2], fm.detect_nodes_of_step(test_flow, "first_step", nodes))
        self.assertEqual(nodes[:2], fm.detect_nodes_of_step(test_flow, "second_step", nodes))
        self.assertEqual(nodes[:2], fm.detect_nodes_of_step(test_flow, "last_step", nodes))

        test_flow = self.simple_test_flow1()
        test_flow.ops[0].where = "instance1"
        test_flow.ops[1].where = "instance1, instance2"
        test_flow.ops[2].where = "instance1;instance2,"
        self.assertEqual(nodes[:1], fm.detect_nodes_of_step(test_flow, "first_step", nodes))
        self.assertEqual(nodes[:2], fm.detect_nodes_of_step(test_flow, "second_step", nodes))
        self.assertEqual([], fm.detect_nodes_of_step(test_flow, "last_step", nodes))

    def simple_test_flow1(self):
        return FlowEntity("test_flow1", [
            FlowOperationEntity("first_step", "sensor_temperature", None, None),
            FlowOperationEntity("second_step", None, "log", None),
            FlowOperationEntity("last_step", None, None, "exit"),
        ])

    def simple_test_flow2(self):
        return FlowEntity("test_flow2", [
            FlowOperationEntity("first_step", "sensor_temperature", None, None, "instance1,instance2"),
            FlowOperationEntity("second_step", None, "cep_flow", None, "*", "x < 10"),
            FlowOperationEntity("third_step", None, "log", None),
            FlowOperationEntity("last_step", None, None, "actuator_speaker", "*", "1"),
        ])

    def simple_test_flow3(self):
        return FlowEntity("test_flow3", [
            FlowOperationEntity("first_step", "sensor_temperature", None, None),
            FlowOperationEntity("last_step", None, None, "exit"),
        ])


if __name__ == '__main__':
    unittest.main()

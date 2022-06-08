import json
import unittest
import os
from json import JSONDecodeError

import pime2.database as db
from typing import List
from pime2.config import load_app_config
from pime2.repository.flow_repository import FlowRepository
from pime2.entity import FlowEntity
from pime2.entity import FlowOperationEntity
from sqlite3 import Error, IntegrityError

from pime2.service.node_service import NodeService
from pime2.service.flow_service import FlowService
from pime2.mapper.flow_mapper import FlowMapper


class FlowRepositoryTest(unittest.TestCase):
    connection = None
    flow_repo = None

    @classmethod
    def setUp(cls):
        if os.path.exists("testDatabase.db"):
            db.disconnect(cls.connection)
            os.remove("testDatabase.db")
        cls.connection = db.create_connection("testDatabase.db")
        load_app_config("me.yaml")
        cls.flow_repo = FlowRepository(cls.connection)
        cls.flow_service = FlowService()
        cls.flow_mapper = FlowMapper()
        cls.node_service = NodeService()
        db.create_default_tables(cls.connection, cls.node_service)
        cls.flow_repo.delete_all()
        cls.node_service.delete_all_nodes()


    def get_flow_list(self) -> List[FlowEntity]:
        return [
            FlowEntity("flow1", [
                FlowOperationEntity(name='Flow_op_one', input='Input', process='Process', output='Output', where='*',
                                    join="join", args='Args'),
                FlowOperationEntity(name='Flow_op_two', input='Input', process='Process', output='Output', where='*',
                                    join="join", args='Args'),
                FlowOperationEntity(name='Flow_op_three', input='Input', process='Process', output='Output', where='*',
                                    join="join", args='Args')]),
            FlowEntity("flow2", [
                FlowOperationEntity(name='Flow_op_two', input='Input', process='Process', output='Output', where='*',
                                    join="join", args='Args'),
                FlowOperationEntity(name='Flow_op_three', input='Input', process='Process', output='Output', where='*',
                                    join="join", args='Args')]),
            FlowEntity("flow3", [
                FlowOperationEntity(name='Flow_op_one', input='Input', process='Process', output='Output', where='*',
                                    join="join", args='Args')]),
            FlowEntity("flow4", []),
            FlowEntity("flow5"),
            FlowEntity("flow6", [
                FlowOperationEntity(name='Flow_op_one', input='Input', process='Process', output='Output', where='*',
                                    join="join", args='Args'),
                FlowOperationEntity(name='Flow_op_two', input='Input', process='Process', output='Output', where='*',
                                    join="join", args='Args'),
                FlowOperationEntity(name='Flow_op_three', input='Input', process='Process', output='Output', where='*',
                                    join="join", args='Args')]),
            FlowEntity("flow7", [
                FlowOperationEntity(name='Flow_op_one', input='Input', process='Process', output='Output', where='*',
                                    join="join", args='Args'),
                FlowOperationEntity(name='Flow_op_two', input='Input', process='Process', output='Output', where='*',
                                    join="join", args='Args'),
                FlowOperationEntity(name='Flow_op_three', input='Input', process='Process', output='Output', where='*',
                                    join="join", args='Args')])]

    def get_flow_list_update(self) -> List[FlowEntity]:
        return [
            FlowEntity("flow1", [
                FlowOperationEntity(name='Flow_op_one', input='Input', process='Process', output='Output', where='*',
                                    join="join", args='x>0'),
                FlowOperationEntity(name='Flow_op_two', input='Input', process='log', output='Output', where='*',
                                    join="join", args='Args'),
                FlowOperationEntity(name='Flow_op_three', input='Sensor', process='Process', output='Output', where='*',
                                    join="join", args='Args')]),
            FlowEntity("flow2", [
                FlowOperationEntity(name='Flow_op_two', input='Input', process='Process', output='Output', where='*',
                                    join="join", args='Args'),
                FlowOperationEntity(name='Flow_op_three', input='Input', process='Process', output='Output', where='*',
                                    join="join", args='Args')]),
            FlowEntity("flow3", []),
            FlowEntity("flow4", [FlowOperationEntity(name='Flow_op_one', input='Input', process='Process', output='Output', where='*',
                                    join="join", args='Args')]),
            FlowEntity("flow5"),
            FlowEntity("flow6", []),
            FlowEntity("flow7", [
                FlowOperationEntity(name='Flow_op_one', input='Input', process='Process', output='Output', where='127.0.0.1',
                                    join="join", args='Args'),
                FlowOperationEntity(name='Flow_op_two', input='Input', process='Process', output='Output', where='*',
                                    join="join", args='Args'),
                FlowOperationEntity(name='Flow_op_three', input='Input', process='log', output='Output', where='*',
                                    join="join", args='Args')])]
    def get_flow_list_json(self) -> List[str]:
        return [
            '{"name": "flow1", "ops": [{"name": "Flow_op_one", "input": "Input", "process": "Process", "output": "Output", "join": "join", "args": "Args", "where": "*"}, {"name": "Flow_op_two", "input": "Input", "process": "Process", "output": "Output", "join": "join", "args": "Args", "where": "*"}, {"name": "Flow_op_three", "input": "Input", "process": "Process", "output": "Output", "join": "join", "args": "Args", "where": "*"}]}',
            '{"name": "flow2", "ops": [{"name": "Flow_op_two", "input": "Input", "process": "Process", "output": "Output", "join": "join", "args": "Args", "where": "*"}, {"name": "Flow_op_three", "input": "Input", "process": "Process", "output": "Output", "join": "join", "args": "Args", "where": "*"}]}',
            '{"name": "flow3", "ops": [{"name": "Flow_op_one", "input": "Input", "process": "Process", "output": "Output", "join": "join", "args": "Args", "where": "*"}]}',
            '{"name": "flow4", "ops": []}',
            '{"name": "flow5", "ops": []}',
            '{"name": "flow6", "ops": [{"name": "Flow_op_one", "input": "Input", "process": "Process", "output": "Output", "join": "join", "args": "Args", "where": "*"}, {"name": "Flow_op_two", "input": "Input", "process": "Process", "output": "Output", "join": "join", "args": "Args", "where": "*"}, {"name": "Flow_op_three", "input": "Input", "process": "Process", "output": "Output", "join": "join", "args": "Args", "where": "*"}]}',
            '{"name": "flow7", "ops": [{"name": "Flow_op_one", "input": "Input", "process": "Process", "output": "Output", "join": "join", "args": "Args", "where": "*"}, {"name": "Flow_op_two", "input": "Input", "process": "Process", "output": "Output", "join": "join", "args": "Args", "where": "*"}, {"name": "Flow_op_three", "input": "Input", "process": "Process", "output": "Output", "join": "join", "args": "Args", "where": "*"}]}',
        ]

    def get_simple_flow(self):
        return FlowEntity("simple_flow", [FlowOperationEntity(name='Flow_op_one', input='Input', process='Process', output='Output', where='*',join="join", args='Args')])

    def get_simple_flow_json(self):
        return '{"name": "simple_flow", "ops": [{"name": "Flow_op_one", "input": "Input", "process": "Process", "output": "Output", "join": "join", "args": "Args", "where": "*"}]}'

    def test_get_all_flows(self):
        flow_list = self.get_flow_list()
        for flow in flow_list:
            self.flow_service.put_flow(flow)
        result = self.flow_service.get_all_flows()
        self.assertEqual(flow_list, result)

    def test_get_all_flows_empty(self):
        self.assertEqual([], self.flow_service.get_all_flows())

    def test_put_simple_flow_entity(self):
        simple_flow = self.get_simple_flow()
        self.flow_service.put_flow(simple_flow)
        result = self.flow_service.get_all_flows()
        self.assertEqual(simple_flow, result[0])

    def test_put_flow_type_error(self):
        with self.assertRaises(TypeError):
            self.flow_service.put_flow(1234)

    def test_put_simple_flow_json(self):
        simple_flow = self.get_simple_flow()
        simple_flow_json = self.get_simple_flow_json()
        self.flow_service.put_flow(simple_flow_json)
        result = self.flow_service.get_all_flows()
        self.assertEqual(simple_flow, result[0])

    def test_delete_all_flows(self):
        flow_list = self.get_flow_list()
        for flow in flow_list:
            self.flow_service.put_flow(flow)
        result = self.flow_service.get_all_flows()
        self.assertEqual(flow_list, result)
        self.flow_service.delete_all_flows()
        result = self.flow_service.get_all_flows()
        self.assertEqual(0, result.__len__())

    def test_remove_flow_entity(self):
        flow_list = self.get_flow_list()
        for flow in flow_list:
            self.flow_service.put_flow(flow)
        result = self.flow_service.get_all_flows()
        self.assertEqual(flow_list, result)
        self.flow_service.remove_flow(flow_list[0])
        self.assertIsNone(self.flow_repo.read_flow_by_name("flow1"))
        with self.assertRaises(Error):
            self.flow_service.remove_flow(self.get_simple_flow())

    def test_remove_flow_json(self):
        flow_list = self.get_flow_list()
        flow_list_json = self.get_flow_list_json()
        for flow in flow_list_json:
            self.flow_service.put_flow(flow)
        result = self.flow_service.get_all_flows()
        self.assertEqual(flow_list, result)
        self.flow_service.remove_flow(flow_list_json[0])
        self.assertIsNone(self.flow_repo.read_flow_by_name("flow1"))
        self.assertFalse(self.flow_service.remove_flow('{"name""flow4", "ops"[]}'))
        self.assertFalse(self.flow_service.remove_flow(123))

    @classmethod
    def tearDownClass(cls):
        db.disconnect(cls.connection)
        os.remove("testDatabase.db")


if __name__ == '__main__':
    unittest.main()

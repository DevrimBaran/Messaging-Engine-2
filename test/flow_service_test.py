import unittest

from typing import List
from pime2.repository.flow_repository import FlowRepository
from pime2.entity import FlowEntity
from pime2.entity import FlowOperationEntity
from sqlite3 import Error

from pime2.service.node_service import NodeService
from pime2.service.flow_service import FlowService
from pime2.mapper.flow_mapper import FlowMapper
from test.generic import GenericDatabaseTest


class FlowRepositoryTest(GenericDatabaseTest):
    connection = None
    flow_repo = None
    node_service = None

    @classmethod
    def setUp(cls):
        super().setUp()
        cls.flow_repo = FlowRepository(cls.connection)
        cls.flow_service = FlowService()
        cls.flow_mapper = FlowMapper()
        cls.node_service = NodeService()
        cls.flow_repo.delete_all()
        cls.node_service.delete_all_nodes()

    def get_flow_list(self) -> List[FlowEntity]:
        return [
            FlowEntity("flow1", [
                FlowOperationEntity(name='Flow_op_one', input='Input', where='*', args='Args')]),
            FlowEntity("flow2", [
                FlowOperationEntity(name='Flow_op_one', input='Input', where='*', args='Args'),
                FlowOperationEntity(name='Flow_op_two', output='Output', where='*', args='Args')]),
            FlowEntity("flow3", [FlowOperationEntity(name='Flow_op_one', input='Input', where='*'),
                                 FlowOperationEntity(name='Flow_op_two', join='Join', where='*')]),
            FlowEntity("flow4", [FlowOperationEntity(name='Flow_op_one', input='Input', where='*'),
                                 FlowOperationEntity(name='Flow_op_two', join='Join', where='*', args="Args")]),
            FlowEntity("flow5", [FlowOperationEntity(name='Flow_op_one', input='Input', where='*')]),
            FlowEntity("flow6", [
                FlowOperationEntity(name='Flow_op_one', input='Input', where='*', ),
                FlowOperationEntity(name='Flow_op_two', process='Process', where='*'),
                FlowOperationEntity(name='Flow_op_three', output='Output', where='*')]),
            FlowEntity("flow7", [
                FlowOperationEntity(name='Flow_op_one', input='Input', where='*', args='Args'),
                FlowOperationEntity(name='Flow_op_two', process='Process', where='*', args='Args'),
                FlowOperationEntity(name='Flow_op_three', output='Output', where='*', args='Args')])]

    def get_flow_list_json(self) -> List[str]:
        return [
            '{"name": "flow1", "ops": [{"name": "Flow_op_one", "input": "Input", "args": "Args", "where": "*"}]}',
            '{"name": "flow2", "ops": [{"name": "Flow_op_one", "input": "Input", "args": "Args", "where": "*"},{"name": "Flow_op_two", "output": "Output", "args": "Args", "where": "*"}]}',
            '{"name": "flow3", "ops": [{"name": "Flow_op_one", "input": "Input", "where": "*"},{"name": "Flow_op_two", "join": "Join", "where": "*"}]}',
            '{"name": "flow4", "ops": [{"name": "Flow_op_one","input": "Input","where": "*"},{"name": "Flow_op_two","join": "Join","where": "*","args": "Args"}]}',
            '{"name": "flow5", "ops": [{"name": "Flow_op_one", "input": "Input", "where": "*"}]}',
            '{"name": "flow6","ops": [{"name": "Flow_op_one","input": "Input","where": "*"},{"name": "Flow_op_two","process": "Process","where": "*"},{"name": "Flow_op_three", "output": "Output","where": "*"}]}',
            '{"name": "flow7", "ops": [{"name": "Flow_op_one", "input": "Input", "where": "*", "args": "Args"},{"name": "Flow_op_two", "process": "Process", "args": "Args", "where": "*"},{"name": "Flow_op_three", "output": "Output", "args": "Args", "where": "*"}]}'
        ]

    def get_flow_list_update(self) -> List[FlowEntity]:
        return [
            FlowEntity("flow1", [
                FlowOperationEntity(name='Flow_op_one', input='Input', where='*', args='x>0'),
                FlowOperationEntity(name='Flow_op_two', process='log', where='*', args='Args'),
                FlowOperationEntity(name='Flow_op_three', output='Output', where='*', args='Args')]),
            FlowEntity("flow2", [
                FlowOperationEntity(name='Flow_op_two', input='Input', output='Output', where='*', args='Args'),
                FlowOperationEntity(name='Flow_op_three', input='Input', process='Process', where='*')]),
            FlowEntity("flow3", [FlowOperationEntity(name='Flow_op_one', input='Input', where='*')]),
            FlowEntity("flow4", [FlowOperationEntity(name='Flow_op_one', input='Input', where='*')]),
            FlowEntity("flow5", [FlowOperationEntity(name='Flow_op_one', input='Input', where='*')]),
            FlowEntity("flow6", [FlowOperationEntity(name='Flow_op_one', input='Input', where='*')]),
            FlowEntity("flow7", [
                FlowOperationEntity(name='Flow_op_one', input='Input', where='127.0.0.1'),
                FlowOperationEntity(name='Flow_op_two', process='Process', where='*', args='x > 5'),
                FlowOperationEntity(name='Flow_op_three', output='Output', where='*')])]

    def get_simple_flow(self):
        return FlowEntity("simple_flow",
                          [FlowOperationEntity(name='Flow_op_one', input='Input', where='*', args='Args')])

    def get_simple_flow_json(self):
        return '{"name": "simple_flow", "ops": [{"name": "Flow_op_one", "input": "Input", "args": "Args", "where": "*"}]}'

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

if __name__ == '__main__':
    unittest.main()

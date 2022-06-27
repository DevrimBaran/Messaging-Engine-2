import unittest
from typing import List
from pime2.repository.flow_repository import FlowRepository
from pime2.entity import FlowEntity
from pime2.entity import FlowOperationEntity
from sqlite3 import Error

from pime2.service.node_service import NodeService
from test.generic import GenericDatabaseTest


class FlowRepositoryTest(GenericDatabaseTest):
    connection = None
    flow_repo = None
    node_service = None

    @classmethod
    def setUp(cls):
        super().setUp()

        cls.flow_repo = FlowRepository(cls.connection)
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
        return FlowEntity("simple_flow", [
            FlowOperationEntity(name='Flow_op_one', input='Input', process='Process', output='Output', where='*',
                                join="join", args='Args')])

    def test_read_flow_by_name(self):
        simple_flow = self.get_simple_flow()
        self.flow_repo.create_flow(simple_flow)
        result_flow = self.flow_repo.read_flow_by_name("simple_flow")
        self.assertEqual(simple_flow, result_flow)
        result_flow_none = self.flow_repo.read_flow_by_name("Test")
        self.assertIsNone(result_flow_none)

    def test_read_all_flows(self):
        flow_list = self.get_flow_list()
        for flow in flow_list:
            self.flow_repo.create_flow(flow)
        result = self.flow_repo.read_all_flows()
        self.assertEqual(flow_list, result)

    def test_read_all_flows_empty(self):
        self.assertEqual([], self.flow_repo.read_all_flows())

    def test_create_simple_flow(self):
        simple_flow = self.get_simple_flow()
        self.flow_repo.create_flow(simple_flow)
        result = self.flow_repo.read_all_flows()
        self.assertEqual(simple_flow, result[0])

    def test_create_duplicate_flow(self):
        simple_flow = self.get_simple_flow()
        self.flow_repo.create_flow(simple_flow)
        self.flow_repo.create_flow(simple_flow)
        self.assertEqual(1, len(self.flow_repo.read_all_flows()))

    def test_delete_all(self):
        flow_list = self.get_flow_list()
        for flow in flow_list:
            self.flow_repo.create_flow(flow)
        result = self.flow_repo.read_all_flows()
        self.assertEqual(flow_list, result)
        self.flow_repo.delete_all()
        result = self.flow_repo.read_all_flows()
        self.assertEqual(0, result.__len__())

    def test_delete_flow_by_name(self):
        flow_list = self.get_flow_list()
        for flow in flow_list:
            self.flow_repo.create_flow(flow)
        result = self.flow_repo.read_all_flows()
        self.assertEqual(flow_list, result)
        self.flow_repo.delete_flow_by_name("flow1")
        self.assertIsNone(self.flow_repo.read_flow_by_name("flow1"))
        with self.assertRaises(Error):
            self.flow_repo.delete_flow_by_name("Test")

    def test_check_in_database(self):
        flow_list = self.get_flow_list()
        for flow in flow_list:
            self.flow_repo.create_flow(flow)
        self.assertEqual(True, self.flow_repo.check_in_database("flow1"))
        self.assertEqual(False, self.flow_repo.check_in_database("Test"))

    def test_update_flow(self):
        flow_list = self.get_flow_list()
        for flow in flow_list:
            self.flow_repo.create_flow(flow)
        self.assertEqual(flow_list, self.flow_repo.read_all_flows())
        flow_list_update = self.get_flow_list_update()
        for flow_update in flow_list_update:
            self.flow_repo.update_flow(flow_update)
        self.assertEqual(flow_list_update, self.flow_repo.read_all_flows())
        with self.assertRaises(Error):
            self.flow_repo.update_flow(FlowEntity("Test", [
                FlowOperationEntity(name='Flow_op_one', input='Input', process='Process', output='Output', where='*',
                                    join="join", args='Args')]))


if __name__ == '__main__':
    unittest.main()

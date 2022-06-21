import unittest

from pime2.flow.flow_manager import FlowManager
from pime2.flow.flow_validation import is_flow_valid
from pime2.service.node_service import NodeService
from test.generic import GenericDatabaseTest


class FlowManagerTest(GenericDatabaseTest):

    @classmethod
    def setUp(cls):
        super().setUp()

    def test_defined_nodes_are_valid(self):
        fm = FlowManager(NodeService())
        for n in fm.get_flows():
            self.assertTrue(is_flow_valid(n))


if __name__ == '__main__':
    unittest.main()

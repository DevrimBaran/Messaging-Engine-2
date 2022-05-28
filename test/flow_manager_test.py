import unittest
from typing import List

from pime2.flow import FlowManager, FlowValidationService, FlowOperationManager
from pime2.flow.flow_message_builder import FlowMessageBuilder
from pime2.node import NodeManager, NodeEntity


class FlowManagerTest(unittest.TestCase):

    def fm(self) -> FlowManager:
        return FlowManager(FlowValidationService(), FlowOperationManager(), FlowMessageBuilder(), NodeManager())

    def test_get_nodes(self):
        nodes = self.fm().get_nodes()
        self.assertTrue(isinstance(nodes, List))

    def test_get_flows(self):
        nodes = self.fm().get_flows()
        self.assertTrue(isinstance(nodes, List))


if __name__ == '__main__':
    unittest.main()

import unittest

from pime2.config import get_me_conf
from pime2.service.node_service import NodeService
from test.generic import GenericDatabaseTest


class NodeServiceTest(GenericDatabaseTest):
    node_service: NodeService = None

    @classmethod
    def setUp(cls):
        super().setUp()
        cls.node_service = NodeService()
        cls.node_service.delete_all_nodes()

    def test_get_neighbor_and_all_nodes(self):
        self.assertEqual(0, len(self.node_service.get_all_nodes()))
        self.node_service.create_own_node()
        own_node = self.node_service.get_own_node()
        self.assertIsNotNone(own_node)
        self.assertEqual(1, len(self.node_service.get_all_nodes()))
        self.assertEqual(0, len(self.node_service.get_all_neighbor_nodes()))
        instance_id = get_me_conf().instance_id
        self.assertEqual(instance_id, own_node.name)
        self.assertIsNotNone(self.node_service.node_repository.read_node_by_name(instance_id))


if __name__ == '__main__':
    unittest.main()

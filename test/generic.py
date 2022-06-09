import os
import unittest

from pime2 import database
from pime2.config import load_app_config
from pime2.repository.node_repository import NodeRepository
from pime2.service.node_service import NodeService


class GenericDatabaseTest(unittest.TestCase):
    connection = None

    @classmethod
    def setUp(cls):
        if os.path.exists("testDatabase.db"):
            database.disconnect(cls.connection)
            os.remove("testDatabase.db")
        load_app_config("me.yaml")
        cls.connection = database.create_connection("testDatabase.db")
        database.create_default_tables(cls.connection, NodeService())

    @classmethod
    def tearDownClass(cls) -> None:
        database.disconnect(cls.connection)
        os.remove("testDatabase.db")

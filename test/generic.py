import os
import unittest

from me2 import database
from me2.config import load_app_config
from me2.service.node_service import NodeService

TEST_DATABASE_FILE = "testDatabase.db"


class GenericDatabaseTest(unittest.TestCase):
    connection = None

    @classmethod
    def setUp(cls):
        if os.path.exists(TEST_DATABASE_FILE):
            database.disconnect(cls.connection)
            os.remove(TEST_DATABASE_FILE)
        load_app_config("me.yaml")
        cls.connection = database.create_connection(TEST_DATABASE_FILE)
        database.create_default_tables(cls.connection, NodeService())

    @classmethod
    def tearDownClass(cls) -> None:
        database.disconnect(cls.connection)
        os.remove(TEST_DATABASE_FILE)

import unittest
import os
import pime2.database as db


class DatabaseTest(unittest.TestCase):
    connection = None

    @classmethod
    def setUpClass(cls):
        cls.connection = db.create_connection("testDatabase.db")

    def test_create_default_tables(self):
        db.create_default_tables(self.connection)

        sql_insert_testdata = """INSERT INTO nodes (id, name, ip, port)
                                    VALUES 
                                        (1, 'node1', "10.10.10.1", 5683),
                                        (2, 'node2', "10.10.10.2", 5683),
                                        (3, 'node3', "10.10.10.3", 5683);"""

        sql_select_testdata = """SELECT * FROM nodes"""

        cursor = self.connection.cursor()
        cursor.execute(sql_insert_testdata)
        cursor.execute(sql_select_testdata)
        self.connection.commit()

        result = cursor.fetchall()
        cursor.close()

        self.assertEqual(
            [(1, 'node1', '10.10.10.1', 5683), (2, 'node2', "10.10.10.2", 5683), (3, 'node3', "10.10.10.3", 5683)],
            result)

    @classmethod
    def tearDownClass(cls):
        db.disconnect(cls.connection)
        os.remove("testDatabase.db")


if __name__ == '__main__':
    unittest.main()

import unittest
import os
import pime2.database as db


class DatabaseTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.connection = db.create_connection("testDatabase.db")
        cls.cursor = cls.connection.cursor()

    def test_create_connection(self):
        self.assertTrue(self.cursor)

    def test_create_default_tables(self):
        db.create_default_tables(self.connection, self.cursor)

        sql_insert_testdata = """INSERT INTO sensors (id, name)
                                    VALUES 
                                        (1, 'temperature sensor'),
                                        (2, 'hall sensor'),
                                        (3, 'buzzer');"""

        sql_select_testdata = """SELECT * FROM sensors"""

        self.cursor.execute(sql_insert_testdata)
        self.cursor.execute(sql_select_testdata)
        self.connection.commit()

        result = self.cursor.fetchall()
        self.assertEqual([(1, 'temperature sensor'), (2, 'hall sensor'), (3, 'buzzer')], result)

    @classmethod
    def tearDownClass(cls):
        cls.cursor.close()
        db.disconnect(cls.connection)
        os.remove("testDatabase.db")


if __name__ == '__main__':
    unittest.main()

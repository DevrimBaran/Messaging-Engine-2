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

        sql_insert_testdata = """INSERT INTO sensors (id, name)
                                    VALUES 
                                        (1, 'temperature sensor'),
                                        (2, 'hall sensor'),
                                        (3, 'buzzer');"""

        sql_select_testdata = """SELECT * FROM sensors"""

        cursor = self.connection.cursor()
        cursor.execute(sql_insert_testdata)
        cursor.execute(sql_select_testdata)
        self.connection.commit()

        result = cursor.fetchall()
        cursor.close()

        self.assertEqual([(1, 'temperature sensor'), (2, 'hall sensor'), (3, 'buzzer')], result)

    @classmethod
    def tearDownClass(cls):
        db.disconnect(cls.connection)
        os.remove("testDatabase.db")


if __name__ == '__main__':
    unittest.main()

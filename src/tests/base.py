import unittest

from peewee import SqliteDatabase

test_db = SqliteDatabase(':memory:')


class TestCase(unittest.TestCase):
    MODELS = []

    def setUp(self):
        # Bind model classes to test db. Since we have a complete list of
        # all models, we do not need to recursively bind dependencies.

        test_db.bind(self.MODELS, bind_refs=False, bind_backrefs=False)

        test_db.connect()
        test_db.create_tables(self.MODELS)

    def tearDown(self):
        # Not strictly necessary since SQLite in-memory databases only live
        # for the duration of the connection, and in the next step we close
        # the connection...but a good practice all the same.
        test_db.drop_tables(self.MODELS)

        # Close connection to db.
        test_db.close()

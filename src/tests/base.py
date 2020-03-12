import unittest

from peewee import SqliteDatabase

test_db = SqliteDatabase(':memory:')


class TestCase(unittest.TestCase):
    MODELS = []

    def setUp(self):
        # Cambia la base de datos a una que se encuentra en memoria
        # Solo funciona con la lista de modelos que se configura por TestCase

        test_db.bind(self.MODELS, bind_refs=False, bind_backrefs=False)

        test_db.connect()
        test_db.create_tables(self.MODELS)

    def tearDown(self):
        # Innecesario, pero buena practica
        test_db.drop_tables(self.MODELS)
        test_db.close()

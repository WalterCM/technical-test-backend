import os
import bottle

from src import models
from src.utils.cors import EnableCors

# El siguiente import no se usa explicitamente.
# Solo es colocado aqui para el routing
import src.urls


def initialize_db():
    db = models.db
    db.connect()
    db.create_tables([models.User, models.Note], safe=True)
    db.close()


# try:
#     os.remove('notes_app.db')
# except FileNotFoundError:
#     pass

initialize_db()

bottle.install(EnableCors())
bottle.run(host='localhost', port=8000, debug=True)

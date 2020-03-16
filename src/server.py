import os
import bottle

from src import models

# El siguiente import no se usa explicitamente.
# Solo es colocado aqui para el routing
import src.urls


def initialize_db():
    db = models.db
    db.connect()
    db.create_tables([models.User, models.Note], safe=True)
    db.close()


try:
    os.remove('notes_app.db')
except FileNotFoundError:
    pass

initialize_db()


@bottle.route('/<:re:.*>', method='OPTIONS')
def enable_cors_generic_route():
    add_cors_headers()


@bottle.hook('after_request')
def enable_cors_after_request_hook():
    add_cors_headers()


def add_cors_headers():
    bottle.response.headers['Access-Control-Allow-Origin'] = '*'
    bottle.response.headers['Access-Control-Allow-Methods'] = \
        'GET, POST, PUT, OPTIONS'
    bottle.response.headers['Access-Control-Allow-Headers'] = \
        'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'


bottle.run(host='localhost', port=8000, debug=True)

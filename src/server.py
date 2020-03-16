import os
import bottle

from src import models
from src import views
from src.utils.routing import path

urlpatterns = [
    path('users/token/', views.UserTokenView, name='users.token'),
    path('users/create/', views.CreateUserView, name='users.create'),
    path('notes/create/', views.CreateNoteView, name='notes.create'),
    path('notes/<id:int>/manage/', views.ManageNoteView, name='notes.manage'),
    path('notes/list/', views.ListNotesView, name='notes.list')
]


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

bottle.run(host='localhost', port=8000, debug=True)

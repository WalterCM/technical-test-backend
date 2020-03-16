import bottle

from .utils.routing import path
from . import views


urlpatterns = [
    path('users/token/', views.UserTokenView, name='users.token'),
    path('users/create/', views.CreateUserView, name='users.create'),
    path('notes/create/', views.CreateNoteView, name='notes.create'),
    path('notes/<id:int>/manage/', views.ManageNoteView, name='notes.manage'),
    path('notes/list/', views.ListNotesView, name='notes.list')
]


bottle.run(host='localhost', port=8000, debug=True)

import bottle

from .utils.routing import path
from . import views


urlpatterns = [
    path('users/create/', views.CreateUserView, name='users.create')
]


bottle.run(host='localhost', port=8000, debug=True)

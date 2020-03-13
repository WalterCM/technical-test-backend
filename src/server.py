import bottle

from .utils.routing import path
from . import views


urlpatterns = [
    path('users/create/', views.TestView, name='test')
]


bottle.run(host='localhost', port=8000, debug=True)

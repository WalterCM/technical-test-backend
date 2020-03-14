from .utils import views
from src import serializers


class CreateUserView(views.CreateAPIView):
    serializer_class = serializers.UserSerializer


class CreateNoteView(views.CreateAPIView):
    serializer_class = serializers.NoteSerializer

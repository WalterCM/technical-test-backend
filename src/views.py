from .utils import views
from src import serializers
from src import models


class CreateUserView(views.CreateAPIView):
    serializer_class = serializers.UserSerializer


class CreateNoteView(views.CreateAPIView):
    serializer_class = serializers.NoteSerializer


class ListNotesView(views.ListAPIView):
    serializer_class = serializers.NoteSerializer
    queryset = models.Note.select()

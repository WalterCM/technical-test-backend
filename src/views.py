from .utils import views
from src import serializers
from src import models

from src.utils import permissions


class CreateUserView(views.CreateAPIView):
    serializer_class = serializers.UserSerializer


class CreateNoteView(views.CreateAPIView):
    serializer_class = serializers.NoteSerializer
    permission_classes = (permissions.IsAuthenticated,)


class ListNotesView(views.ListAPIView):
    serializer_class = serializers.NoteSerializer
    queryset = models.Note.select()

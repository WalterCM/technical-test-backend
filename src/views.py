from .utils import views
from src import serializers
from src import models

from src.utils import permissions


class UserTokenView(views.CreateAPIView):
    serializer_class = serializers.TokenSerializer


class CreateUserView(views.CreateAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.AllowAny,)


class CreateNoteView(views.CreateAPIView):
    serializer_class = serializers.NoteSerializer
    permission_classes = (permissions.IsAuthenticated,)


class ListNotesView(views.ListAPIView):
    serializer_class = serializers.NoteSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Note.select()


class ManageNoteView(views.RetrieveUpdateAPIView):
    serializer_class = serializers.NoteSerializer
    permissions = (permissions.IsAuthenticated,)

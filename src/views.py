from .utils import views
from src import serializers

from src.utils import permissions


class UserTokenView(views.CreateAPIView):
    serializer_class = serializers.TokenSerializer


class CreateUserView(views.CreateAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.AllowAny,)


class CreateNoteView(views.CreateAPIView):
    serializer_class = serializers.NoteSerializer
    permission_classes = (permissions.IsAuthenticated,)


class ManageNoteView(views.RetrieveUpdateAPIView):
    serializer_class = serializers.NoteSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return self.user.notes


class ListNotesView(views.ListAPIView):
    serializer_class = serializers.NoteSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return self.user.notes

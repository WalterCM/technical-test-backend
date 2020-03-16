from bottle import request

from src.utils import status
from src.utils import permissions
from src.utils.response import response


class PermissionException(Exception):
    pass


class BaseAPIView:
    args = None
    kwargs = None

    methods = None
    serializer_class = None
    queryset = None
    permission_classes = None

    user = None

    lookup_field = 'id'

    def __init__(self):
        if not self.permission_classes:
            self.permission_classes = [permissions.AllowAny]

    def permission_denied(self, message,
                          status_code=status.HTTP_403_FORBIDDEN):
        response(
            message,
            status=status_code
        )
        raise PermissionException

    def get_permissions(self):
        return [permission() for permission in self.permission_classes]

    def check_permissions(self):
        for permission in self.get_permissions():
            if not permission.has_permission(self):
                self.permission_denied(
                    permission.errors,
                    status.HTTP_401_UNAUTHORIZED
                )

    def check_object_permissions(self, obj):
        for permission in self.get_permissions():
            if not permission.has_object_permission(self, obj):
                self.permission_denied(permission.errors)

    def callback(self, *args, **kwargs):
        try:
            self.check_permissions()
        except PermissionException:
            return

        self.args = args
        self.kwargs = kwargs

        try:
            res = getattr(self, request.method.lower())(*args, **kwargs)
            return res
        except PermissionException:
            pass

    def get_object(self):
        queryset = self.get_queryset()

        assert self.lookup_field in self.kwargs,  (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, self.lookup_field)
        )

        lookup_value = self.kwargs.get(self.lookup_field)
        obj = queryset.model.get_or_none(
            getattr(queryset.model, self.lookup_field) == lookup_value
        )

        self.check_object_permissions(obj)

        return obj

    def get_queryset(self):
        assert self.queryset is not None, (
                "'%s' should either include a `queryset` attribute, "
                "or override the `get_queryset()` method."
                % self.__class__.__name__
        )

        return self.queryset

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def get_serializer_context(self):
        return {
            'user': self.user
        }

    def get_serializer_class(self):
        assert self.serializer_class is not None, (
            "'%s' should either include a `serializer_class` attribute, "
            "or override the `get_serializer_class()` method."
            % self.__class__.__name__
        )

        return self.serializer_class


class CreateAPIView(BaseAPIView):
    methods = ['POST']

    def post(self):
        serializer = self.get_serializer(data=request.json)
        if serializer.is_valid():
            serializer.save()
            return response(serializer.data, status=status.HTTP_201_CREATED)
        return response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RetrieveUpdateAPIView(BaseAPIView):
    methods = ['GET', 'PUT', 'PATCH']

    def get(self, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return response(serializer.data)

    def put(self, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.json,
            partial=partial
        )
        if serializer.is_valid():
            serializer.save()
            return response(serializer.data)
        return response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, *args, **kwargs):
        kwargs['partial'] = True
        self.put(*args, **kwargs)


class ListAPIView(BaseAPIView):
    methods = ['GET']

    def get(self, *args, **kwargs):
        queryset = self.get_queryset()

        serializer = self.get_serializer(queryset, many=True)
        return response(serializer.data)

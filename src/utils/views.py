from bottle import request

from src.utils import status
from src.utils.response import response


class BaseAPIView:
    methods = []
    serializer_class = None
    queryset = None
    permission_classes = ()
    _permission_classes = []

    def __init__(self):
        for permission in self.permission_classes:
            self._permission_classes.append(permission())

    def callback(self):
        for permission in self._permission_classes:
            if not permission.has_permission():
                return response(
                    permission.errors,
                    status=status.HTTP_401_UNAUTHORIZED
                )

        return getattr(self, request.method.lower())()

    def get_queryset(self):
        assert self.queryset is not None, (
                "'%s' should either include a `queryset` attribute, "
                "or override the `get_queryset()` method."
                % self.__class__.__name__
        )

        return self.queryset

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        return serializer_class(*args, **kwargs)

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


class ListAPIView(BaseAPIView):
    methods = ['GET']

    def get(self):
        queryset = self.get_queryset()

        serializer = self.get_serializer(queryset, many=True)
        return response(serializer.data)

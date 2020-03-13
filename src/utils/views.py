from bottle import request

from src.utils import status
from src.utils.response import response


class BaseAPIView:
    methods = []
    serializer_class = None
    queryset = None

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
        serializer = self.get_serializer(data=dict(request.forms))
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return response(serializer.data, status=status.HTTP_201_CREATED)


class ListAPIView(BaseAPIView):
    methods = ['GET']

    def get(self):
        queryset = self.get_queryset()

        serializer = self.get_serializer(queryset, many=True)
        return response(serializer.data)

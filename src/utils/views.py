class BaseAPIView:
    methods = ['GET']

    def get(self):
        return 'test'


class CreateAPIView(BaseAPIView):
    methods = ['GET']

import bottle
from bottle import response


class EnableCors(object):
    name = 'enable_cors'
    api = 2

    def apply(self, fn, context):
        def _enable_cors(*args, **kwargs):
            # set CORS headers
            origin = 'Access-Control-Allow-Origin'
            methods = 'Access-Control-Allow-Methods'
            headers = 'Access-Control-Allow-Headers'
            response.headers[origin] = '*'
            response.headers[methods] = 'GET, POST, PUT, PATCH, OPTIONS'
            response.headers[headers] = 'Authorization, Origin, Accept, ' \
                                        'Content-Type, X-Requested-With, ' \
                                        'X-CSRF-Token'

            if bottle.request.method != 'OPTIONS':
                # actual request; reply with the actual response
                return fn(*args, **kwargs)

        return _enable_cors

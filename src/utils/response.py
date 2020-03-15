import bottle

from src.utils import status as status_codes


def response(data, status=status_codes.HTTP_200_OK):
    bottle.response.headers['Content-Type'] = 'application/json'
    bottle.response.status = status

    if status >= status_codes.HTTP_400_BAD_REQUEST:
        bottle.abort(status, data)

    return data

import bottle

from src.utils import status as status_codes


def response(data, status=status_codes.HTTP_200_OK):
    if status >= status_codes.HTTP_400_BAD_REQUEST:
        bottle.abort(status, data)

    return {
        'data': data,
        'status_code': status
    }

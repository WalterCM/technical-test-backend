from src.utils import status as status_codes


def response(data, status=status_codes.HTTP_200_OK):
    return {
        'data': data,
        'status_code': status
    }

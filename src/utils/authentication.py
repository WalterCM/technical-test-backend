from bottle import request

from src import conf

jwtsecret = conf.SECRET


class AuthorizationError(Exception):
    pass


def jwt_token_from_header():
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthorizationError('Authorization header is expected')

    parts = auth.split()

    if parts[0].lower() != 'bearer':
        raise AuthorizationError('Authorization header must start with Bearer')
    elif len(parts) == 1:
        raise AuthorizationError('Token not found')
    elif len(parts) > 2:
        raise AuthorizationError('Authorization header must be Bearer token')

    return parts[1]

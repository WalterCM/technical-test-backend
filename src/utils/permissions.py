import jwt

from src.utils.authentication import jwt_token_from_header
from src.utils.authentication import AuthorizationError
from src.utils.authentication import jwtsecret


class BasePermission:
    _errors = []

    def has_permission(self):
        return True

    def has_object_permission(self):
        return True

    @property
    def errors(self):
        errors = []
        for error in self._errors:
            if hasattr(error, 'messages'):
                errors += error.messages
            else:
                errors.append(error.args)

        return errors


class IsAuthenticated(BasePermission):
    def has_permission(self):
        token = None
        try:
            token = jwt_token_from_header()
        except AuthorizationError as e:
            self._errors.append(e)
            return False

        try:
            jwt.decode(token, jwtsecret)  # throw away value
        except jwt.ExpiredSignature:
            self._errors.append('token is expired')
            return False
        except jwt.DecodeError as e:
            self._errors.append(e)
            return False

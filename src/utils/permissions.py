import jwt

from src import conf
from src.utils.authentication import jwt_token_from_header


class BasePermission:
    _errors = []

    def check_permission(self):
        try:
            permission = self.has_permission()
        except Exception as e:
            self._errors.append(e)
            permission = False

        return permission

    def check_object_permission(self, obj):
        try:
            permission = self.has_object_permission(obj)
        except Exception as e:
            self._errors.append(e)
            permission = False

        return permission

    def has_permission(self):
        return True

    def has_object_permission(self, obj):
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


class AllowAny(BasePermission):
    pass


class IsAuthenticated(BasePermission):
    def has_permission(self):
        token = jwt_token_from_header()
        jwt.decode(
            token,
            conf.JWT.get('secret'),
            algorithms=conf.JWT.get('algorithm')
        )

        return True

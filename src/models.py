import os
import hashlib
import binascii
import peewee

from src import conf

db = peewee.SqliteDatabase('my_app.db')


class BaseModel(peewee.Model):
    class Meta:
        database = db


class UserManager:
    def create_user(self, username=None, password=None):
        if not username:
            raise ValueError('User requires username')
        if not password:
            raise ValueError('User requires password')

        if len(password) < conf.MIN_PASSWORD_LENGTH:
            raise ValueError(
                'Password requires a min length of {}'.format(
                    conf.MIN_PASSWORD_LENGTH
                )
            )

        user = User(username=username)
        user.set_password(password)
        user.save()

        return user


class User(BaseModel):
    username = peewee.CharField(unique=True)
    password = peewee.CharField()

    objects = UserManager()

    def set_password(self, new_password):
        """Funcion que setea el password de usuario"""
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        password_hash = hashlib.pbkdf2_hmac(
            'sha512',
            new_password.encode('utf-8'),
            salt,
            100000
        )
        password_hash = binascii.hexlify(password_hash)
        self.password = (salt + password_hash).decode('ascii')
        self.save()

    def check_password(self, password_to_check):
        """Funcion que chequea si el password es correcto"""
        salt = self.password[:64]
        password_hash = hashlib.pbkdf2_hmac(
            'sha512',
            password_to_check.encode('utf-8'),
            salt.encode('ascii'),
            100000
        )
        password_hash = binascii.hexlify(password_hash).decode('ascii')
        return password_hash == self.password[64:]

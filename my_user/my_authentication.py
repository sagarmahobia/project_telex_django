from rest_framework.authentication import BaseAuthentication

from my_user.jwt_user import JwtUser
from my_user.models import User


class JwtAuthentication(BaseAuthentication):
    def authenticate(self, request, username=None, password=None):
        auth = request.META.get('HTTP_AUTHORIZATION', b'')
        token = auth[7:]

        decode = JwtUser.decode(token)
        user = User()
        user.id = decode.id
        user.role = decode.role
        return user, None


class NoAuthentication(BaseAuthentication):
    def authenticate(self, request, username=None, password=None):
        user = User()
        return user, None

import jwt

from my_user.models import User


class JwtUser:
    id = 0
    role = ""
    name = ""

    @staticmethod
    def get_key():
        return "OBl@keXLincon"

    def to_dict(self):
        return {"id": self.id, "role": self.role, "user_name": self.name}

    def to_token(self):
        return jwt.encode(self.to_dict(), JwtUser.get_key(), algorithm="HS256")

    def to_user(self):
        return User(id=self.id, role=self.role)

    @staticmethod
    def decode(token):
        jwt_user = jwt.decode(token, JwtUser.get_key(), algorithms="HS256")
        user = JwtUser()

        user.id = jwt_user["id"]
        user.role = jwt_user["role"]
        return user

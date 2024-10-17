from jose import jwt
from ..config import jwtsettings
from datetime import datetime, timedelta

class JwtControler():
    """Класс по работе с токенами"""
    def __init__(self):
        """Init file."""
        self.jwt_sekret_key = jwtsettings.JWT_SEKRET_KEY
        self.algoritm = jwtsettings.ALGORITM
        self.access_time = jwtsettings.ACCESS_TIME
        self.refresh_time = jwtsettings.REFRESH_TIME

    def create_access_token(self, id: int, role: list[str]):
        """Создание access token.

        Args:
            id (int): id пользователя
            role (list[str]): массив ролей

        Returns:
            access_tokne: access_token
        """
        exp = datetime.now() + timedelta(minutes=self.access_time)
        jwt_decode = {'exp': exp, 'user_id': id, 'role': role}
        return jwt.encode(jwt_decode, self.jwt_sekret_key, self.algoritm)

    def create_refresh_token(self, id: int, role: list[str]):
        """Создание refresh token.

        Args:
            id (int): апользователя
            role (list[str]): массив ролей

        Returns:
            refresh_tokne: refresh_token
        """
        exp = datetime.now() + timedelta(days=self.refresh_time)
        jwt_decode = {'exp': exp, 'user_id': id, 'role': role}
        return jwt.encode(jwt_decode, self.jwt_sekret_key, self.algoritm)

    def validate_tokens(self, token):
        """Валидация токена.

        Args:
            token (str): access_token

        Returns:
            data: данные о токене
        """
        try:
            return jwt.decode(token, self.jwt_sekret_key, self.algoritm)
        except Exception:
            return False


jwtcontroler = JwtControler()

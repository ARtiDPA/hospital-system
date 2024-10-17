from jose import jwt
from ..config import jwtsettings
from datetime import datetime, timedelta

class JwtControler():
    """Класс по работе с токенами"""
    def __init__(self):
        self.jwt_sekret_key = jwtsettings.JWT_SEKRET_KEY
        self.algoritm = jwtsettings.ALGORITM
        self.access_time = jwtsettings.ACCESS_TIME
        self.refresh_time = jwtsettings.REFRESH_TIME

    
    def create_access_token(self, id):
        exp = datetime.now() + timedelta(minutes=self.access_time)
        jwt_decode = {'exp': exp, 'user_id': id}
        return jwt.encode(jwt_decode, self.jwt_sekret_key, self.algoritm)

    def create_refresh_token(self, id):
        exp = datetime.now() + timedelta(days=self.refresh_time)
        jwt_decode = {'exp': exp, 'user_id': id}
        return jwt.encode(jwt_decode, self.jwt_sekret_key, self.algoritm)


jwtcontroler = JwtControler()
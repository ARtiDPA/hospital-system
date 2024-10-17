"""Маршрутизаторы аккаунтов."""
from fastapi import APIRouter

from ...db import pgsql
from fastapi import HTTPException

route = APIRouter()


@route.post('/SignUp')
def sign_up(
    firstname: str,
    lastname: str,
    username: str,
    password: str,
):
    """Маршрутизатор регистрации.

    Args:
        firstname (str): имя
        lastname (str): фамилия
        username (str): название аккаунта
        password (str): пароль

    Raises:
        HTTPException: 409, пользователь с таким именем уже сущетсвует

    Returns:
        json: the account has been created
    """
    if not pgsql.get_user_by_username(username):
        pgsql.create_user(firstname, lastname, username, password)
        return {'message': 'the account has been created'}
    raise HTTPException(
        409,
        'A user with that name has already been registered',
        )
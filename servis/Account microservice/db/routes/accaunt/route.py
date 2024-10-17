"""Маршрутизаторы аккаунтов."""
from fastapi import APIRouter

from ...db import pgsql
from fastapi import HTTPException
from ...auth.hash import hashed
from ...auth.tokens import jwtcontroler

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
    if not pgsql.check_user_in_db(username):
        pgsql.create_user(firstname, lastname, username, password, accesslevel=0)
        return {'message': 'the account has been created'}
    raise HTTPException(
        409,
        'A user with that name has already been registered',
        )


@route.post('/SignIn')
def sign_in(
    username: str,
    password: str,
):
    """Маршрутизатор входа.

    Args:
        username (str): логин
        password (str): пароль

    Raises:
        HTTPException: 409 пароли не совпадают
        HTTPException: 404 пользователь не зарегистрирован

    Returns:
        json: access/refresh токены
    """
    user = pgsql.get_user_by_username(username)
    if user:
        if hashed.chech_hash(password, user.password):
            access_token = jwtcontroler.create_access_token(user.id)
            refresh_token = jwtcontroler.create_refresh_token(user.id)

            pgsql.add_tokens_in_bd(user.id, access_token, refresh_token)

            return {
                'access_token': access_token,
                'refresh_token': refresh_token,
            }
        raise HTTPException(403, "passwords don't match")
    raise HTTPException(404, 'the user is not registered')

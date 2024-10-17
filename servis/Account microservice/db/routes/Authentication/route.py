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
        pgsql.create_user(
            firstname,
            lastname,
            username,
            password,
            role=['user'],
            )
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
            access_token = jwtcontroler.create_access_token(user.id, user.role)
            refresh_token = jwtcontroler.create_refresh_token(
                user.id,
                user.role,
                )

            pgsql.add_tokens_in_bd(user.id, access_token, refresh_token)

            return {
                'access_token': access_token,
                'refresh_token': refresh_token,
            }
        raise HTTPException(403, "passwords don't match")
    raise HTTPException(404, 'the user is not registered')


@route.put('/SignOut')
def sign_out(access_token: str):
    """Маршрутизатор выхода.

    Args:
        access_token (str): access_token

    Raises:
        HTTPException: 409
        HTTPException: 401

    Returns:
        json: Вы вышли
    """
    if access_token:
        data = jwtcontroler.validate_tokens(access_token)
        if data:
            pgsql.delete_tokens_in_bd(data.get('user_id'))
            return {'message': "You're out"}
        raise HTTPException(400, 'Tokens error.')
    raise HTTPException(401, 'Unauthorized.')


@route.get('/Validate')
def validate(access_token: str):
    """Марщрутизатор проверки токена.

    Args:
        access_token (str): access_token

    Raises:
        HTTPException: 400

    Returns:
        json: данные токена
    """
    user = jwtcontroler.validate_tokens(access_token)
    if user:
        return user
    raise HTTPException(400, 'Tokens error.')

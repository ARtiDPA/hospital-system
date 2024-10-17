from fastapi import APIRouter
from ...auth.tokens import jwtcontroler
from ...db import pgsql
from fastapi import HTTPException
from ...models import User
from ...auth.hash import hashed



route = APIRouter()


@route.get('/Me')
def info_by_me(access_token):
    """Маршрутизатор получение информаци об аккаунте.

    Args:
        access_token (str): access token

    Raises:
        HTTPException: 400

    Returns:
        json: вся информаци об пользователе
    """
    payload = jwtcontroler.validate_tokens(access_token)
    if payload:
        user_data = pgsql.get_user_by_id(payload.get('user_id'))
        return {
            'firstname': user_data.firstname,
            'lastname': user_data.lastname,
            'username': user_data.username,
            'role': user_data.role,
        }

    raise HTTPException(400, 'Tokens error')


@route.put('/Update')
def update_info(
    access_token: str,
    firstname: str,
    lastname: str,
    username: str,
    password: str,
):
    """Маршрутизатор обновления данных.

    Args:
        access_token (str): access_token
        firstname (str): имя
        lastname (str): фамилия
        username (str): название акакунта
        password (str): пароль пользователя

    Raises:
        HTTPException: 400

    Returns:
        json: the data has been updated
    """
    payload = jwtcontroler.validate_tokens(access_token)
    if payload:
        user = User(
            id=payload.get('user_id'),
            firstname=firstname,
            lastname=lastname,
            username=username,
            password=password,
            )
        pgsql.update_data(user)
        return {'message': 'the data has been updated'}
    raise HTTPException(400, 'Tokens error')


@route.get('Accounts')
def get_all_accounts(access_token: str)
    payload = jwtcontroler.validate_tokens(access_token)
    if payload:
        if 'admin' in payload.get('role'):
            pass
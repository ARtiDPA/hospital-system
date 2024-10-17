"""Модели для валидации данных."""
from pydantic import BaseModel


class TokensModels(BaseModel):
    """Модель данных регистрации.

    Args:
        BaseModel (class): базовая модель
    """

    access_token: str
    refresh_token: str

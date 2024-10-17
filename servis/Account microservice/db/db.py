"""Файл для работы с базой данных."""
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from .config import pgsqlsettings
from .models import Base, User

from db.auth.hash import hashed

class PostgresDataBase():
    """Файл для работь с бд."""

    def __init__(self) -> None:
        """Init func."""
        self.dsn = '{driver}://{user}:{password}@{host}:{port}/{name}'.format(
            driver=pgsqlsettings.db_driver,
            name=pgsqlsettings.db_name,
            password=pgsqlsettings.db_password,
            host=pgsqlsettings.db_host,
            port=pgsqlsettings.db_port,
            user=pgsqlsettings.db_user,
        )

        self.engine = create_engine(self.dsn)

    def create_all_tables(self) -> bool:
        """Создание таблиц в бд.

        Returns:
            bool: статус выполнения функции.
        """
        try:
            Base.metadata.create_all(self.engine, checkfirst=True)
        except Exception:
            return False
        return True

    def create_user(
            self,
            firstname,
            lastname,
            username,
            password,
            ) -> bool:
        """Добавление пользователя в бд.

        Args:
            firstname (str): имя
            lastname (str): фамилия
            username (str): имя аккаунта
            password (str): пароль

        Returns:
            bool: результат выполнения функции
        """
        password = hashed.create_hash(password)

        newuser = User(
            firstname=firstname,
            lastname=lastname,
            username=username,
            password=password,
            )
        with Session(self.engine) as session:
            try:
                session.add(newuser)
                session.commit()
                session.refresh(newuser)
            except Exception:
                return False
            else:
                return True

    def get_user_by_username(self, username):
        """Проверка на наличие пользователя в БД.

        Args:
            username (str): логин пользователя

        Returns:
            bool: true/false если ли пользователь
        """
        with Session(self.engine) as session:
            user = session.query(User).filter(User.username == username).first()
            return True if user else False


pgsql = PostgresDataBase()

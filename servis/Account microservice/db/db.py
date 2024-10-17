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
            firstname: str,
            lastname: str,
            username: str,
            password: str,
            role: list[str],
            ) -> bool:
        """Добавление пользователя в бд.

        Args:
            firstname (str): имя
            lastname (str): фамилия
            username (str): имя аккаунта
            password (str): пароль
            role (list): массив ролей

        Returns:
            bool: результат выполнения функции
        """
        password = hashed.create_hash(password)

        newuser = User(
            firstname=firstname,
            lastname=lastname,
            username=username,
            password=password,
            role=role,
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

    def check_user_in_db(self, username):
        """Проверка на наличие пользователя в БД.

        Args:
            username (str): логин пользователя

        Returns:
            bool: true/false если ли пользователь
        """
        with Session(self.engine) as session:
            user = session.query(User).filter(User.username == username).first()
            return True if user else False

    def get_user_by_username(self, username: str):
        """Полечение данных о пользователе по логину.

        Args:
            username (str): логин

        Returns:
            User: данные о пользователе
        """
        with Session(self.engine) as session:
            return session.query(User).filter(User.username == username).first()

    def get_user_by_id(self, user_id: int):
        """Полечение данных о пользователе по id.

        Args:
            user_id(int): id пользователя

        Returns:
            User: данные о пользователе
        """
        with Session(self.engine) as session:
            return session.query(User).filter(User.id == user_id).first()

    def add_tokens_in_bd(
            self,
            user_id: str,
            access_token: str,
            refresh_token: str,
            ):
        """Добавление токенов пользователю.

        Args:
            user_id (str): id пользователя
            access_token (str): access_token
            refresh_token (str): refresh_token
        """
        with Session(self.engine) as session:
            user = session.query(User).filter(User.id == user_id).first()
            user.access_token = access_token
            user.refresh_token = refresh_token
            session.add(user)
            session.commit()
            session.refresh(user)

    def delete_tokens_in_bd(
            self,
            user_id: str,
    ):
        """Удаление пары токенов.

        Args:
            user_id (str): айди пользователя
        """
        with Session(self.engine) as session:
            user = session.query(User).filter(User.id == user_id).first()
            user.access_token = ''
            user.refresh_token = ''
            session.add(user)
            session.commit()
            session.refresh(user)

    def update_data(self, user_data: User):
        with Session(self.engine) as session:
            user = session.query(User).filter(User.id == user_data.id).first()
            user.firstname = user_data.firstname
            user.lastname = user_data.lastname
            user.username = user_data.username
            user.password = hashed.create_hash(user_data.password)
            session.add(user)
            session.commit()
            session.refresh(user)


pgsql = PostgresDataBase()

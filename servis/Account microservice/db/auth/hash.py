import bcrypt


class HashedData():
    """Класс по работе с хэш."""

    def __init__(self):
        """Init file."""
        self.salt = bcrypt.gensalt()

    def create_hash(self, password: str) -> str:
        """Хэширование паоля.

        Args:
            password (str): пароль пользователя

        Returns:
            str: хэшированный пароль
        """
        return bcrypt.hashpw(password.encode('utf-8'), self.salt).decode('utf-8')
    
    def chech_hash(self, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


hashed = HashedData()
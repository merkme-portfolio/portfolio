from typing import Optional, Union

from fastapi import Depends, Request
from fastapi_users import (
    BaseUserManager,
    FastAPIUsers,
    IntegerIDMixin,
    InvalidPasswordException
)
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy
)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.constants import MIN_PASSWORD_LENGHT
from app.core.db import get_async_session
from app.models.user import User
from app.schemas.user import UserCreate


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    """Возвращает объект SQLAlchemyUserDatabase.

    Параметры:
    - session: Сессия для взаимодействия с базой данных.

    Возвращает объект SQLAlchemyUserDatabase для работы с пользователями
    в базе данных.
    """
    yield SQLAlchemyUserDatabase(session, User)

bearer_transport = BearerTransport(tokenUrl='auth/jwt/login')


def get_jwt_strategy() -> JWTStrategy:
    """
    Возвращает объект JWTStrategy для аутентификации.

    Возвращает объект JWTStrategy с настройками из конфигурации приложения.
    """
    return JWTStrategy(secret=settings.secret, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    """Менеджер пользователей."""

    async def validate_password(
        self,
        password: str,
        user: Union[UserCreate, User],
    ) -> None:
        """
        Проверяет пароль пользователя на валидность.

        Параметры:
        - password: Пароль для проверки.
        - user: Объект пользователя или его схема.

        Выбрасывает InvalidPasswordException в случае нарушения правил пароля.
        """
        if len(password) < MIN_PASSWORD_LENGHT:
            raise InvalidPasswordException(
                reason='Password should be at least 3 characters'
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason='Password should not contain e-mail'
            )

    async def on_after_register(
        self,
        user: User,
        request: Optional[Request] = None
    ):
        """
        Вызывается после успешной регистрации пользователя.

        Параметры:
        - user: Зарегистрированный пользователь.
        - request: Запрос, вызвавший регистрацию (опционально).
        """
        print(f'Пользователь {user.email} зарегистрирован.')


async def get_user_manager(user_db=Depends(get_user_db)):
    """
    Возвращает менеджер пользователей.

    Параметры:
    - user_db: Объект базы данных пользователей.

    Возвращает объект UserManager для работы с пользователями.
    """
    yield UserManager(user_db)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """Модель данных для чтения информации о пользователе."""


class UserCreate(schemas.BaseUserCreate):
    """Модель данных для создания нового пользователя."""


class UserUpdate(schemas.BaseUserUpdate):
    """Модель данных для обновления информации о пользователе."""

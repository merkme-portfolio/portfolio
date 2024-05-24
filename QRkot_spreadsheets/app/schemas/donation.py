from datetime import datetime
from typing import Optional

from pydantic import BaseModel, NonNegativeInt, PositiveInt


class DonationCreate(BaseModel):
    """Модель данных для создания нового пожертвования."""

    full_amount: PositiveInt
    comment: Optional[str]

    class Config:
        """
        Конфигурация схемы Pydantic.

        Параметры:
        - orm_mode (bool): Указывает Pydantic, что модель используется
        для работы с данными из ORM.
        """

        orm_mode = True


class DonationRetrive(DonationCreate):
    """Модель данных для получения информации о пожертвовании."""

    id: int
    create_date: datetime


class DonationDB(DonationRetrive):
    """Модель данных для хранения информации о пожертвовании в базе данных."""

    user_id: int
    invested_amount: NonNegativeInt
    fully_invested: bool
    close_date: Optional[datetime]
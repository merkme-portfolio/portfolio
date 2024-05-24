from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, NonNegativeInt, PositiveInt

from app.core.constants import (
    USERNAME_LMAX,
    USERNAME_LMIN,
    MIN_FIELD_LENGTH
)


class CharityProjectBase(BaseModel):
    """Базовая схема данных для благотворительного проекта."""

    name: str = Field(..., min_length=USERNAME_LMIN, max_length=USERNAME_LMAX)
    description: str = Field(..., min_length=MIN_FIELD_LENGTH)
    full_amount: PositiveInt

    class Config:
        """
        Конфигурация схемы Pydantic.

        При установке значения Extra.forbid,
        Pydantic будет выдавать ошибку при обнаружении дополнительных полей,
        не указанных в модели.
        """

        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    """Схема данных для создания благотворительного проекта."""


class CharityProjectUpdate(CharityProjectBase):
    """Схема данных для обновления благотворительного проекта."""

    name: str = Field(None, min_length=USERNAME_LMIN, max_length=USERNAME_LMAX)
    description: str = Field(None, min_length=MIN_FIELD_LENGTH)
    full_amount: Optional[PositiveInt]


class CharityProjectDB(CharityProjectBase):
    """Схема данных благотворительного проекта в базе данных."""

    id: int
    invested_amount: NonNegativeInt
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        """
        Конфигурация схемы Pydantic.

        Параметры:
        - orm_mode (bool): Указывает Pydantic, что модель используется
        для работы с данными из ORM.
        """

        orm_mode = True
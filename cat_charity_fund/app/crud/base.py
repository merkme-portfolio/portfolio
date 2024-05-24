from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


class CRUDBase:
    """Базовый класс для CRUD-операций."""

    def __init__(self, model):
        """
        Инициализирует объект CRUDBase.

        Параметры:
        - model: ORM-модель для выполнения CRUD-операций.
        """
        self.model = model

    async def get(
        self,
        obj_id: int,
        session: AsyncSession,
    ):
        """
        Получает объект по его идентификатору.

        Параметры:
        - obj_id: Идентификатор объекта.
        - session: Сессия для взаимодействия с базой данных.

        Возвращает объект из базы данных.
        """
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return db_obj.scalars().first()

    async def get_by_attribute(
        self,
        attr_name: str,
        attr_value: str,
        session: AsyncSession,
    ):
        """
        Получает объект по значению определенного атрибута.

        Параметры:
        - attr_name: Имя атрибута.
        - attr_value: Значение атрибута.
        - session: Сессия для взаимодействия с базой данных.

        Возвращает объект из базы данных.
        """
        attr = getattr(self.model, attr_name)
        db_obj = await session.execute(
            select(self.model).where(attr == attr_value)
        )
        return db_obj.scalars().first()

    async def get_multi(
        self,
        session: AsyncSession
    ):
        """
        Получает все объекты из базы данных.

        Параметры:
        - session: Сессия для взаимодействия с базой данных.

        Возвращает список объектов из базы данных.
        """
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
        self,
        obj_in,
        session: AsyncSession,
        user: Optional[User] = None
    ):
        """
        Создает новый объект в базе данных.

        Параметры:
        - obj_in: Данные для создания нового объекта.
        - session: Сессия для взаимодействия с базой данных.
        - user: Пользователь, создающий объект (опционально).

        Возвращает созданный объект из базы данных.
        """
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db_obj,
        obj_in,
        session: AsyncSession,
    ):
        """
        Обновляет объект в базе данных.

        Параметры:
        - db_obj: Объект для обновления.
        - obj_in: Новые данные для объекта.
        - session: Сессия для взаимодействия с базой данных.

        Возвращает обновленный объект из базы данных.
        """
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
        self,
        db_obj,
        session: AsyncSession,
    ):
        """
        Удаляет объект из базы данных.

        Параметры:
        - db_obj: Объект для удаления.
        - session: Сессия для взаимодействия с базой данных.

        Возвращает удаленный объект из базы данных.
        """
        await session.delete(db_obj)
        await session.commit()
        return db_obj

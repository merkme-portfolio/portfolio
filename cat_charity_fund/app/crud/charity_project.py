from datetime import datetime
from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


class CRUDCharityProject(CRUDBase):
    """CRUD операции для благотворительных проектов."""

    async def get_charity_project_by_name(
        self,
        project_name: str,
        session: AsyncSession,
    ) -> Optional[int]:
        """
        Получает идентификатор благотворительного проекта по его имени.

        Параметры:
        - project_name: Имя благотворительного проекта.
        - session: Сессия для взаимодействия с базой данных.
        """
        charity_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        return charity_project_id.scalars().first()

    async def charity_project_update(
        self,
        db_obj: CharityProject,
        obj_in: CharityProjectUpdate,
        session: AsyncSession
    ):
        """
        Обновляет информацию о благотворительном проекте.

        Параметры:
        - db_obj: Объект благотворительного проекта для обновления.
        - obj_in: Новые данные для проекта.
        - session: Сессия для взаимодействия с базой данных.

        Возвращает обновленный объект благотворительного проекта.
        """
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        if db_obj.invested_amount == db_obj.full_amount:
            db_obj.fully_invested = True
            db_obj.close_date = datetime.now()

        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj


charity_project_crud = CRUDCharityProject(CharityProject)

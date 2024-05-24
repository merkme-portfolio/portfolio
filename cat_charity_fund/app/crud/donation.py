from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User


class CRUDDonation(CRUDBase):
    """CRUD операции для пожертвований."""

    async def get_donations_by_user(
        self,
        session: AsyncSession,
        user: User
    ) -> Donation:
        """
        Получает пожертвования пользователя.

        Параметры:
        - session: Сессия для взаимодействия с базой данных.
        - user: Пользователь, чьи пожертвования нужно получить.

        Возвращает список пожертвований пользователя из базы данных.
        """
        db_objs = await session.execute(
            select(self.model).where(
                self.model.user_id == user.id
            )
        )
        return db_objs.scalars().all()


donation_crud = CRUDDonation(Donation)
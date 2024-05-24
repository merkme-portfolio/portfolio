from datetime import datetime
from typing import List, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def invest_in_projects_or_donations(
    obj_to_invest: Union[CharityProject, Donation],
    session: AsyncSession
) -> Union[CharityProject, Donation]:
    """
    Инвестирует в благотворительные проекты или пожертвования.

    Параметры:
    - obj_to_invest: Проект благотворительности или пожертвование.
    - session: Асинхронная сессия для взаимодействия с базой данных.

    Возвращает объект после инвестирования.
    """
    invested_model = CharityProject if isinstance(
        obj_to_invest, Donation
    ) else Donation

    not_invested_objects = await get_not_invested_objects(
        invested_model, session
    )

    if not_invested_objects:
        available_investment_amount = obj_to_invest.full_amount
        for obj in not_invested_objects:
            remaining_amount_needed = obj.full_amount - obj.invested_amount
            investment_amount = min(
                remaining_amount_needed, available_investment_amount
            )
            available_investment_amount -= investment_amount

            obj.invested_amount += investment_amount

            if obj.full_amount == obj.invested_amount:
                close_invested_object(obj)

            if not available_investment_amount:
                close_invested_object(obj_to_invest)
                break

        await session.commit()

    return obj_to_invest


async def get_not_invested_objects(
    model_type: Union[CharityProject, Donation],
    session: AsyncSession
) -> List[Union[CharityProject, Donation]]:
    """
    Получает список непроинвестированных объектов проектов или пожертвований.

    Параметры:
    - model_type: Тип модели благотворительного проекта или пожертвования.
    - session: Асинхронная сессия для взаимодействия с базой данных.

    Возвращает список объектов проектов или пожертвований,
    которые не были проинвестированы.
    """
    query = select(
        model_type
    ).where(
        model_type.fully_invested.is_(False)
    ).order_by(
        model_type.create_date
    )
    objects = await session.execute(query)
    return objects.scalars().all()


def close_invested_object(obj: Union[CharityProject, Donation]) -> None:
    """
    Закрывает проинвестированный благотворительный проект или пожертвование.

    Параметры:
    - obj: Проект или пожертвование.
    """
    obj.fully_invested = True
    obj.close_date = datetime.now()
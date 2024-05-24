from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import INVESTED_DEFAULT
from app.core.enums.errors import ValidationError
from app.crud.charity_project import charity_project_crud
from app.models import CharityProject


async def check_name_duplicate(
    project_id: str,
    session: AsyncSession,
) -> None:
    """Проверка имени проекта на дублирование."""
    room_id = await charity_project_crud.get_charity_project_by_name(
        project_id,
        session,
    )

    if room_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=ValidationError.project_name_already_exist,
        )


async def check_charity_project_exists(
    charity_project_id: int,
    session: AsyncSession,
) -> CharityProject:
    """Проверяет существование проекта по id."""
    charity_project = await charity_project_crud.get(
        charity_project_id,
        session
    )
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=ValidationError.project_not_found
        )
    return charity_project


async def check_charity_project_before_update(
    charity_project: CharityProject,
    full_amount: int
) -> None:
    """
    Выполяет необходимые проверки перед изменениями.

    Не может быть изменён если:
        - требуемая сумма меньше уже внесённой
        - проект собрал все средства или был закрыт
    """
    if full_amount and full_amount < charity_project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=ValidationError.project_full_amout_not_valid
        )
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=ValidationError.project_already_invested.format('изменить')
        )


async def check_charity_project_before_delete(
    charity_project: CharityProject,
) -> None:
    """
    Выполяет необходимые проверки перед изменениями.

    Не может быть изменён если:
        - в проект были внесены средства (в любом количестве)
        - проект собрал все средства или был закрыт
    """
    if charity_project.invested_amount > INVESTED_DEFAULT:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=ValidationError.project_already_invested.format('удалить')
        )
    if charity_project.fully_invested or charity_project.close_date:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=ValidationError.project_closed_or_fully_invested
        )

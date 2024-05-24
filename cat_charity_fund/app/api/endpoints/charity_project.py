from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_charity_project_before_delete,
    check_charity_project_before_update,
    check_charity_project_exists,
    check_name_duplicate
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate
)
from app.services.investition import invest_in_projects_or_donations

router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectDB],
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    """Возвращает список всех проектов благотворительности."""
    return await charity_project_crud.get_multi(session)


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Создает новый проект благотворительности.

    Доступ к энд-поинту:
        - Только для суперпользователей
    """
    await check_name_duplicate(charity_project.name, session)
    new_project = await charity_project_crud.create(charity_project, session)
    await invest_in_projects_or_donations(new_project, session)
    await session.refresh(new_project)
    return new_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def remove_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Удаляет проект благотворительности.

    Доступ к энд-поинту:
        - Только для суперпользователей
    """
    charity_project = await check_charity_project_exists(
        project_id,
        session,
    )
    await check_charity_project_before_delete(charity_project)
    return await charity_project_crud.remove(
        charity_project,
        session,
    )


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Частично обновляет информацию о проекте благотворительности.

    Доступ к энд-поинту:
        - Только для суперпользователей
    """
    charity_project = await check_charity_project_exists(
        project_id, session
    )

    if obj_in.name != charity_project.name:
        await check_name_duplicate(obj_in.name, session)

    await check_charity_project_before_update(
        charity_project,
        obj_in.full_amount
    )

    charity_project = await charity_project_crud.charity_project_update(
        charity_project, obj_in, session
    )
    await session.refresh(charity_project)
    return charity_project
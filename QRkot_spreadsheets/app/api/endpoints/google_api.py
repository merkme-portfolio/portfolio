from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.services.google_api import (
    set_user_permissions,
    spreadsheets_create,
    spreadsheets_update_value,
    spreadsheets_list,
    spreadsheets_clear_disk
)

router = APIRouter()

GOOGLE_SHEETS_URL = 'https://docs.google.com/spreadsheets/d/'


@router.post(
    '/',
    dependencies=[Depends(current_superuser)],
)
async def get_spreadsheet_report(
    google_object: Aiogoogle = Depends(get_service),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Только для суперпользователей.

    Формирует отчет по закрытым благотворительным проектам.
    """
    projects = await charity_project_crud.get_projects_by_completion_rate(
        session
    )
    spreadsheet_id = await spreadsheets_create(google_object)
    await set_user_permissions(spreadsheet_id, google_object)
    await spreadsheets_update_value(spreadsheet_id, projects, google_object)
    return f'{GOOGLE_SHEETS_URL}{spreadsheet_id}'


@router.get(
    '/',

)
async def get_all_spreadsheets(
    google_object: Aiogoogle = Depends(get_service)
):
    """
    Только для суперпользователей.

    Выводит все отчёты по проекту QRKot.
    """
    return await spreadsheets_list(google_object)


@router.delete(
    '/',
    dependencies=[Depends(current_superuser)],
)
async def delete_all_not_last(
    google_object: Aiogoogle = Depends(get_service)
):
    """
    Только для суперпользователей.

    Удаляет все отчёты по проекту QRKot, кроме последнего.
    """
    return await spreadsheets_clear_disk(google_object, save_last=True)


@router.delete(
    '/clear_disk',
    dependencies=[Depends(current_superuser)],
)
async def delete_all_spreadsheets(
    google_object: Aiogoogle = Depends(get_service)
):
    """
    Только для суперпользователей.

    Удаляет все отчёты по проекту QRKot.
    """
    return await spreadsheets_clear_disk(google_object, save_last=False)

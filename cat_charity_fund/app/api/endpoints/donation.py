from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import DonationCreate, DonationDB, DonationRetrive
from app.services.investition import invest_in_projects_or_donations

router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationDB],
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    """Возвращает список всех проектов благотворительности."""
    return await donation_crud.get_multi(session)


@router.get(
    path='/my',
    response_model=list[DonationRetrive],
    response_model_exclude_none=True
)
async def get_user_donations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Вернуть список пожертвований пользователя, выполняющего запрос."""
    return await donation_crud.get_donations_by_user(
        user=user,
        session=session
    )


@router.post(
    path='/',
    response_model=DonationRetrive,
)
async def create_donation(
    donation: DonationCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Сделать пожертвование."""
    new_donation = await donation_crud.create(
        obj_in=donation, user=user, session=session
    )
    await invest_in_projects_or_donations(new_donation, session)
    await session.refresh(new_donation)
    return new_donation
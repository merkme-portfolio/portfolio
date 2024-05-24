from sqlalchemy import Column, String, Text

from app.core.absctract_models import CharityDonationBase
from app.core.constants import USERNAME_LMAX


class CharityProject(CharityDonationBase):
    """Модель благотворительного проекта."""

    name = Column(String(USERNAME_LMAX), unique=True, nullable=False)
    description = Column(Text, nullable=False)
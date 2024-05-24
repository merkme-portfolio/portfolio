from sqlalchemy import Column, ForeignKey, Text

from app.core.absctract_models import CharityDonationBase


class Donation(CharityDonationBase):
    """Модель пожертвования."""

    user_id = Column(ForeignKey('user.id'), nullable=False)
    comment = Column(Text)
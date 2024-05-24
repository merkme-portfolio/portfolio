from datetime import datetime as dt

from sqlalchemy import Boolean, Column, DateTime, Integer

from app.core.constants import INVESTED_DEFAULT
from app.core.db import Base


class CharityDonationBase(Base):
    """Базовая модель для благотворительных проектов и пожертвований."""

    __abstract__ = True

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=INVESTED_DEFAULT)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=dt.now)
    close_date = Column(DateTime)

import calendar
import datetime
import logging
from typing import Optional, List, Any

import dateutil.parser
import pytz
from sqlalchemy import select
from sqlalchemy import (Column, Integer, String, DateTime, Boolean)
from sqlalchemy.orm import Session

from birfday import config


class Birthday(config.Base):
    """Birthday model."""

    __tablename__ = "birthdays"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    month = Column(Integer, nullable=False)
    day = Column(Integer, nullable=False)
    note = Column(String)
    dt_created = Column(DateTime, default=datetime.datetime.utcnow())
    dt_updated = Column(DateTime, default=datetime.datetime.utcnow())

    @classmethod
    def create_birthday(
        cls, first_name: str, last_name: str, month: int, day: int,
        note: Optional[str] = None, dt_updated: Optional[str] = None
    ) -> "Birthday":
        """ Creates a Birthday object.

        Args:
            first_name: str, The person's first name.
            last_name: str, The person's last name.
            month: int, The numeric representation of the month (1-12).
            day: int, The numeric representation of the day (1-31).
            note: str, A note associated with this person (e.g. X's husband).
            dt_updated: str, Datetime string for the update date of this
                record in UTC time.
        Returns:
            An instantiated Birthday instance.
        """
        if month not in range(1, 13):
            raise ValueError("Month must be between 1 and 12 inclusive.")

        if day not in range(1, 32):
            raise ValueError("Day must be between 1 and 31 inclusive.")

        data_dict = {
            "first_name": first_name,
            "last_name": last_name,
            "month": month,
            "day": day,
            "note": note,
        }

        if dt_updated is not None:
            data_dict["dt_updated"] = dateutil.parser.parse(
                dt_updated).replace(tzinfo=pytz.utc)

        return cls(**data_dict)


    @classmethod
    def get_birthdays_for_month(
        cls, session: Session, month: int
    ) -> List["Birthday"]:
        """Queries the database to get all records with a birthday in month.

        Args:
            session: An initialized SQLAlchemy session object.
            month: int, The month to search (most likely the current month).
        Returns:
            All database records with birthdays in month.
        """
        return session.execute(
            select(cls).where(cls.month == month)
        ).scalars().all()

    def __str__(self):
        """Format a birthday string as mrkdwn so we can easily send messages."""
        fmt = (
            f"*{self.first_name} {self.last_name}* ("
            f"{calendar.month_name[self.month]} {self.day})"
        )

        if self.note:
            fmt += f":\n_{self.note}_"

        return fmt

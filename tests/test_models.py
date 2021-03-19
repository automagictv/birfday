import datetime
import random

import factory
import pytest
import pytz
from sqlalchemy import orm
from sqlalchemy import create_engine

from birfday import config
from birfday import models


# DB Setup
engine = create_engine("sqlite://")
Session = orm.scoped_session(orm.sessionmaker(bind=engine))
config.Base.metadata.create_all(engine)


# Fixture definitions used in individual tests
@pytest.fixture(scope='module')
def connection():
    """Create an isolated connection that closes itself after each test."""
    connection = engine.connect()
    yield connection
    connection.close()


@pytest.fixture(scope='function')
def session(connection):
    """Create an isolated session that levereages our connection each test."""
    transaction = connection.begin()
    session = Session()
    yield session
    session.close()
    transaction.rollback()


FAKE_DATE_TIME = datetime.datetime(2021, 5, 1, 1, 1, 1, tzinfo=pytz.utc)


@pytest.fixture
def fake_datetime_utcnow(monkeypatch):
    """Fake datetime.datetime.utcnow()."""

    class newutcdatetime:
        @classmethod
        def utcnow(cls):
            return FAKE_DATE_TIME


class BirthdayFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Birthday
        sqlalchemy_session = Session

    id = factory.LazyAttribute(lambda _: random.randrange(1000,9999))
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    month = factory.Faker("pyint", min_value=1, max_value=12)
    day = factory.Faker("pyint", min_value=1, max_value=31)
    note = factory.Faker("sentence")
    dt_created = factory.Faker("date_time")
    dt_updated = factory.Faker("date_time")


class TestBirthdayModel:

    def test_create_birthday_creates_without_kwargs(self, session):
        """Tests that our classmethod actually creates a Birthday object."""
        first_name = "first"
        last_name = "last"
        month = 5
        day = 2
        note = "fake note"

        test_obj = models.Birthday.create_birthday(
            first_name, last_name, month, day, note
        )

        assert test_obj.first_name == first_name
        assert test_obj.last_name == last_name
        assert test_obj.month == month
        assert test_obj.day == day
        assert test_obj.note == note
        assert test_obj.dt_created == FAKE_DATE_TIME
        assert test_obj.dt_updated == FAKE_DATE_TIME

    def test_create_birthday_creates_with_kwargs(self, session):
        """Tests that our classmethod actually creates a Birthdayy object."""
        first_name = "first"
        last_name = "last"
        month = 5
        day = 2
        note = "fake note"
        dt_created = "2021-05-05"
        dt_updated = "2021-05-05 05:05:05"

        test_obj = models.Birthday.create_birthday(
            first_name, last_name, month, day, note, dt_created=dt_created,
            dt_updated=dt_updated
        )

    def test_get_birthdays_for_month_returns_birthdays(self, session):
        """Tests that our classmethod queries and returns birthdays."""
        fake_birthday_month = 5

        bday1 = BirthdayFactory.create()
        bday2 = BirthdayFactory.create()
        bday3 = BirthdayFactory.create()

        bday1.month = 1
        bday2.month = 3
        bday3.month = fake_birthday_month

        results = models.Birthday.get_birthdays_for_month(
            session, fake_birthday_month
        )

        assert results == [bday3]

    def test_get_birthdays_for_month_returns_none(self, session):
        """Tests that we return an empty list if there are no birthdays."""
        bday1 = BirthdayFactory.create()
        bday2 = BirthdayFactory.create()
        bday3 = BirthdayFactory.create()

        bday1.month = 3
        bday2.month = 3
        bday3.month = 3

        results = models.Birthday.get_birthdays_for_month(session, 1)
        assert results == []

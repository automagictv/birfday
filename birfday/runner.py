import calendar
import datetime
import logging

from sqlalchem.orm import SessionTransaction

from birfday import config
from birfday import models
from birfday import db_util
from birfday import telegram_helper

# Set up logging
logging.basicConfig(
    filename=config.LOGFILE,
    level=logging.INFO,
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def main(session: SessionTransaction) -> None:
    #  2. Read database to get birthdays.
    today = datetime.datetime.today()
    birthdays_this_month = models.Birthday.get_birthdays_for_month(
        session, today.month
    )

    birthdays = []
    #  3. See if today is a birthday.
    for birthday in birthdays_this_month:
        if today.day == birthday.day:
            birthdays.append(birthday)
        # Handle leap years
        if (today.month == 2
            and today.day == 28
            and (not calendar.isleap(today.year))
            and birthday.day == 29):
            birthdays.append(birthday)


    #  4. For all birthdays today, notify me and include template message.
    if birthdays:
        bot = telegram_helper.TelegramFacade()
        message = "We've got some birthdays!\n" + "\n".join(
            f"{bday}" for bday in birthdays
        )
        response = bot.send_message(message)
        logging.info(response)


if __name__ == "__main__":
    # Initialize a db session using a context manager and pass it to the main
    # function so we can use it to query / update our database druing runtime.
    # This is executed as one large transaction. See the documentation for more
    # info:
    # https://docs.sqlalchemy.org/en/14/orm/session_basics.html#using-a-sessionmaker 
    with db_util.Session.begin() as session:
        main(session)

import argparse
from argparse import RawTextHelpFormatter
import calendar
import datetime
import logging

import pandas
from sqlalchemy.exc import IntegrityError

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

parser = argparse.ArgumentParser(
    formatter_class=RawTextHelpFormatter,
    description=(
        "CLI for the birfday bot. To execute, simply run the program. "
        "To seed the database, use --mode 'SEED' and --file '/path/to.csv'."
    )
)

parser.add_argument(
    "--mode", type=str, default="RUN", help=(
        "Mode for the application. Defaults to RUN mode. Otherwise, to seed "
        "the database, use SEED mode with the --file argument. When passing in "
        "a csv, make sure the following columns are included:"
        "\n\t`first_name`: String"
        "\n\t`last_name`: String"
        "\n\t`month`: Int - month of the birthday."
        "\n\t`day`: Int - day of the birthday."
        "\n\t`note`: (Optional) String - note about the person."
    )
)

parser.add_argument(
    "--file", type=str, help="A path to a csv file with ',' as the delimiter.",
)


def main(session):
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
        message = "We've got some birthdays!\n\n" + "\n\n".join(
            f"{bday}" for bday in birthdays
        )
        response = bot.send_message(message)
        logging.info(response)


if __name__ == "__main__":
    logging.info("Initializing run...")

    args = parser.parse_args()

    if args.mode == "SEED" and not args.file:
        error = "SEED mode requires a file. Use --file."
        logging.error(error)
        raise ValueError(error)

    # Initialize a db session using a context manager and pass it to the main
    # function so we can use it to query / update our database druing runtime.
    # This is executed as one large transaction. See the documentation for more
    # info:
    # https://docs.sqlalchemy.org/en/14/orm/session_basics.html#using-a-sessionmaker 
    with db_util.Session() as session:
        if args.mode == "SEED":
            logging.info("In seed mode. Reading csv file...")
            df = pandas.read_csv(args.file, sep=",")
            committed = 0

            for _, row in df.iterrows():
                birthday = models.Birthday.create_birthday(dict(row))
                session.add(birthday)

                try:
                    session.commit()
                    committed += 1
                except IntegrityError as e:
                    logging.error(f"DB Integrity error! Skipping record\n{e}")
                    session.rollback()
                    continue

            logging.info(f"Success! Added {committed} birthdays to the db.")

        else:
            main(session)

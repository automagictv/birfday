import logging

from sqlalchem.orm import SessionTransaction

from birfday import config
from birfday import db_util


def main(session: SessionTransaction) -> None:
    pass


if __name__ == "__main__":
    # Initialize a db session using a context manager and pass it to the main
    # function so we can use it to query / update our database druing runtime.
    # This is executed as one large transaction. See the documentation for more
    # info:
    # https://docs.sqlalchemy.org/en/14/orm/session_basics.html#using-a-sessionmaker 
    with db_util.Session.begin() as session:
        main(session)

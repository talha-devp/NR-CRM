import logging
from app.models import db


def create_db(app) -> None:
    with app.app_context():
        db.create_all()


def reset_db(app) -> None:
    with app.app_context():
        logging.critical(msg="Resetting the database")
        print("Resetting the database")
        db.drop_all()
        db.create_all()

from flask import current_app
from sentry_sdk import capture_exception

from stealthx.extensions import db
from .core import core_dao
from .paymongo_payment_transactions import paymongo_pt_dao


def commit():
    try:
        db.session.commit()
        return True
    except Exception as error:
        current_app.logger.error(error)
        db.session.rollback()
        capture_exception(error)


def add_token_and_transact(timestamp, credited_token, **paymongo_info):
    """
    Add token, and create Paymongo transaction entry
    :param timestamp:
    :param credited_token:
    :param paymongo_info:
    :return:
    """
    paymongo_pt_dao.new(timestamp, **paymongo_info)
    core_dao.add_token(credited_token)

from .utils import check_user_status
from flask import request


def user_watcher():
    if request.path != "/confirm-your-email":
        status = check_user_status()
        if status:
            return status

from flask import request

from .utils import check_user_status


def user_watcher():
    if request.path != "/confirm-your-email":
        status = check_user_status()
        if status:
            return status

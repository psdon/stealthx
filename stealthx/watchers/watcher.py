from stealthx.auth.watcher import user_watcher
from flask_login import current_user
from .watchers import subscription_watcher, is_student_watcher

"""
Usage:

@bp.after_request
def _(response):
    return register_watchers(response)

"""


def register_watchers(response):
    if not current_user.is_authenticated:
        return response

    watcher = user_watcher()
    if watcher:
        return watcher

    watcher = subscription_watcher()
    if watcher:
        return watcher

    watcher = is_student_watcher()
    if watcher:
        return watcher

    return response

from stealthx.auth.watcher import user_watcher
from .subscription_watcher import subscription_watcher

"""
Usage:

@bp.after_request
def _(response):
    return register_watchers(response)

"""


def register_watchers(response):
    watcher = user_watcher()
    if watcher:
        return watcher

    watcher = subscription_watcher()
    if watcher:
        return watcher

    return response

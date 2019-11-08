from flask import current_app


def is_url_safe(url):
    for r in current_app.url_map._rules:
        if r.rule == next:
            return url
    return False

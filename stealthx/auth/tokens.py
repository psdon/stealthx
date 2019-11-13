from flask import current_app
from itsdangerous import BadSignature, SignatureExpired
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


def generate_email_token(email, expires_sec=3600):
    s = Serializer(current_app.config["SECRET_KEY"], expires_sec)
    return s.dumps(
        {"email": email}, salt=current_app.config["PASSWORD_SALT_KEY"]
    ).decode("utf-8")


def verify_email_token(token):
    s = Serializer(current_app.config["SECRET_KEY"])
    try:
        email = s.loads(token, current_app.config["PASSWORD_SALT_KEY"])["email"]
    except BadSignature or SignatureExpired:
        return None
    return str(email)

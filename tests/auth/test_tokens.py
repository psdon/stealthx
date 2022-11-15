from stealthx.auth.tokens import generate_email_token, verify_email_token


class TestAuthTokens:

    def test_generate_email_token(self, client):
        token = generate_email_token("admin@mail.com")

        assert "admin@mail.com" == verify_email_token(token)

    def test_invalid_email_token(self, client):
        token = "invalid-token"

        assert verify_email_token(token) is None

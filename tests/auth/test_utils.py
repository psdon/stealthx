from stealthx.auth.utils import create_email_message, send_async_email, send_confirm_email, send_recover_account_email, check_user_status
import pytest
from flask import url_for


@pytest.mark.usefixtures('client')
class TestEmailUtils:

    def test_create_email_message(self):
        msg = create_email_message('test@example.com', 'testing', 'hi')

        assert msg.html == 'hi'

    def test_send_async_email(self):
        outbox = send_async_email('test@example.com', 'testing', 'hi')
        assert outbox[0].subject == 'testing'

    def test_send_confirm_email(self):
        outbox = send_confirm_email("test@example.com")
        assert "Someone, perhaps you, has added this email address (test@example.com) to their Stealth X account." in outbox[0].html

    def test_send_recover_account_email(self):
        outbox = send_recover_account_email("test@example.com")
        assert 'Someone, perhaps you, has made a password reset request for your Stealth X account.' in outbox[0].html


@pytest.mark.usefixtures('client')
class TestMiscUtils:

    def test_check_user_status_not_email_confirmed(self, client, user):
        with client:
            user.email_confirmed = False

            client.post(url_for('auth.sign_in'), data={
                'username_or_email': user.username,
                'password': "a-long-password-987",
            }, follow_redirects=True)

            status = check_user_status()
            assert 302 == status.status_code

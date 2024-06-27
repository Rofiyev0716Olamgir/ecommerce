from django.test import TestCase
from django.conf import settings
from django.contrib.auth.password_validation import validate_password


class SecretKeyTests(TestCase):

    def test_secret_key_strength(self):
        secret = settings.SECRET_KEY
        try:
            validate_password(secret)
        except Exception as e:
            msg = f"Weak secret key, {e.messages}"
            self.fail(msg)


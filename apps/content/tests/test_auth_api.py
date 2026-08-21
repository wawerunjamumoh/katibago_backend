from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


User = get_user_model()


class AuthApiTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            "username": "new-learner",
            "email": "learner@example.com",
            "password": "strong-password-123",
        }

    def test_register_login_me_and_logout(self):
        register_response = self.client.post(
            "/api/v1/auth/register/",
            self.user_data,
            format="json",
        )

        self.assertEqual(register_response.status_code, 201)
        token = register_response.data["token"]
        self.assertTrue(User.objects.filter(username="new-learner").exists())

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
        me_response = self.client.get("/api/v1/auth/me/")
        self.assertEqual(me_response.status_code, 200)
        self.assertEqual(me_response.data["username"], "new-learner")

        logout_response = self.client.post("/api/v1/auth/logout/")
        self.assertEqual(logout_response.status_code, 204)
        self.assertFalse(Token.objects.filter(key=token).exists())

        self.client.credentials()
        unauthenticated_me_response = self.client.get("/api/v1/auth/me/")
        self.assertEqual(unauthenticated_me_response.status_code, 401)

    def test_login_returns_token_for_existing_user(self):
        User.objects.create_user(
            username="existing-learner",
            password="strong-password-123",
        )

        response = self.client.post(
            "/api/v1/auth/login/",
            {
                "username": "existing-learner",
                "password": "strong-password-123",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["token"])

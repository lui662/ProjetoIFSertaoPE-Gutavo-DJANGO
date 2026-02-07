from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.models.contas import Conta

User = get_user_model()

class LoginTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="luiz",
            password="123456",
            tipo_usuario="cliente"
        )

        self.conta, _ = Conta.objects.get_or_create(
            user=self.user,
            defaults={"saldo": 100}
        )

        self.url = reverse("login")

    def test_login_com_credenciais_validas(self):
        response = self.client.post(self.url, {
            "username": "luiz",
            "password": "123456"
        })
        self.assertEqual(response.status_code, 302)

    def test_login_com_senha_errada(self):
        response = self.client.post(self.url, {
            "username": "luiz",
            "password": "errada"
        })
        self.assertEqual(response.status_code, 200)

    def test_login_conta_bloqueada(self):
        self.user.is_active = False
        self.user.save()

        response = self.client.post(self.url, {
            "username": "luiz",
            "password": "123456"
        })
        self.assertEqual(response.status_code, 200)

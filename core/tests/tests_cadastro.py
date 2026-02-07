from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.models.contas import Conta

User = get_user_model()

class CadastroTestCase(TestCase):
    def setUp(self):
        try:
            self.url = reverse("cadastro")
        except:
            try:
                self.url = reverse("register")
            except:
                self.url = reverse("signup")

        self.dados_validos = {
            "username": "novousuario",
            "email": "novo@teste.com",
            "tipo_usuario": "cliente",
            "password1": "Teste@123!",
            "password2": "Teste@123!",
        }

    def test_cadastro_cria_usuario_e_conta(self):
        response = self.client.post(self.url, self.dados_validos)

        if response.context is not None and 'form' in response.context:
             if response.context['form'].errors:
                 print("\nERRO NO CADASTRO:", response.context['form'].errors)

        self.assertTrue(User.objects.filter(username="novousuario").exists())
        
        usuario = User.objects.get(username="novousuario")
        conta_existe = Conta.objects.filter(user=usuario).exists()
        self.assertTrue(conta_existe, "A conta não foi criada automaticamente.")
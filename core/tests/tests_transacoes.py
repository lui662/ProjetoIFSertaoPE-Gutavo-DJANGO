from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from accounts.models.contas import Conta

User = get_user_model()

class TransacaoTestCase(TestCase):
    def setUp(self):

        self.user = User.objects.create_user(username='picpato_user', password='123')
        
        try:
            self.conta = Conta.objects.get(user=self.user)
        except Conta.DoesNotExist:
            self.conta = Conta.objects.create(user=self.user, saldo=0)
            
        self.conta.saldo = 0.00
        self.conta.save()
        
        self.client.force_login(self.user)
        self.url = reverse("depositar") 

    def test_deposito_sucesso(self):
        dados = {
            'valor': '100.00'
        }

        response = self.client.post(self.url, dados)
        
        if response.status_code == 200 and 'form' in response.context:
             if response.context['form'].errors:
                 print("\nERRO NO DEPÓSITO:", response.context['form'].errors)

        self.assertEqual(response.status_code, 302)
        self.conta.refresh_from_db()
        self.assertEqual(self.conta.saldo, 100.00)

    def test_deposito_valor_negativo(self):
        dados = {
            'valor': '-50.00'
        }
        response = self.client.post(self.url, dados)
        
        self.conta.refresh_from_db()
        self.assertEqual(self.conta.saldo, 0.00)
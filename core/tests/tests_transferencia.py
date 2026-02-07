from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.models.contas import Conta

User = get_user_model()

class TransferenciaTestCase(TestCase):

    def setUp(self):

        self.user_remetente = User.objects.create_user(username="remetente", password="123")
        self.user_destinatario = User.objects.create_user(username="destinatario", password="123")

        try:
            self.conta_remetente = Conta.objects.get(user=self.user_remetente)
        except Conta.DoesNotExist:
            self.conta_remetente = Conta.objects.create(user=self.user_remetente, saldo=0)

        try:
            self.conta_destinatario = Conta.objects.get(user=self.user_destinatario)
        except Conta.DoesNotExist:
            self.conta_destinatario = Conta.objects.create(user=self.user_destinatario, saldo=0)

        self.conta_remetente.saldo = 1000
        self.conta_remetente.agencia = "0001"
        self.conta_remetente.numero_conta = "11111" 
        self.conta_remetente.save()
        
        self.conta_destinatario.saldo = 0
        self.conta_destinatario.agencia = "0001"
        self.conta_destinatario.numero_conta = "22222" 
        self.conta_destinatario.save()

        self.url = reverse("transferir") 

    def test_transferencia_sucesso(self):
        self.client.force_login(self.user_remetente)

        dados = {
            "conta_destino": "22222", 
            "agencia": "0001", 
            "valor": 200,
            "descricao": "Transferencia de Teste" 
        }
        
        response = self.client.post(self.url, dados)
        

        if response.context is not None and 'form' in response.context:
             if response.context['form'].errors:
                 print("\nERRO NA TRANSFERÊNCIA:", response.context['form'].errors)
        

        self.conta_remetente.refresh_from_db()
        self.conta_destinatario.refresh_from_db()
        self.assertEqual(self.conta_remetente.saldo, 800)
        self.assertEqual(self.conta_destinatario.saldo, 200)

    def test_transferencia_saldo_insuficiente(self):
        self.client.force_login(self.user_remetente)
        
        dados = {
            "conta_destino": "22222",
            "agencia": "0001", 
            "valor": 1500,
            "descricao": "Tentativa Falha"
        }
        
        response = self.client.post(self.url, dados)
        
        self.conta_remetente.refresh_from_db()
        self.assertEqual(self.conta_remetente.saldo, 1000)
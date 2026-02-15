from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.models.contas import Conta

User = get_user_model()

class FluxoBancarioTestCase(TestCase):
    def setUp(self):
        # Cria os atores do cenário
        self.cliente = User.objects.create_user('cliente_teste', password='123')
        self.recebedor = User.objects.create_user('recebedor_teste', password='123')
        
        self.conta_cliente = Conta.objects.get(user=self.cliente)
        self.conta_cliente.saldo = 1000
        self.conta_cliente.numero_conta = "11111"
        self.conta_cliente.agencia = "0001"
        self.conta_cliente.save()
        
        self.conta_recebedor = Conta.objects.get(user=self.recebedor)
        self.conta_recebedor.numero_conta = "22222"
        self.conta_recebedor.agencia = "0001"
        self.conta_recebedor.save()

    def test_fluxo_completo_transacao(self):

        login = self.client.login(username='cliente_teste', password='123')
        self.assertTrue(login, "Falha no login inicial")

        response_home = self.client.get(reverse('home'))
        self.assertContains(response_home, "1000", msg_prefix="Saldo inicial não exibido corretamente")

        url_transferencia = reverse('transferir')
        dados = {
            "conta_destino": "22222",
            "agencia": "0001",
            "valor": "200.00",
            "descricao": "Pagamento Aluguel"
        }
        
        self.client.post(url_transferencia, dados)
        self.conta_cliente.refresh_from_db()
        self.assertEqual(self.conta_cliente.saldo, 800.00)
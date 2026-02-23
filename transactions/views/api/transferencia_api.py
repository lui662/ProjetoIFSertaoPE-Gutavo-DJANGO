from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import transaction
from transactions.forms.transferencia_forms import TransferenciaForm
from accounts.models.contas import Conta
from core.models import Transacao


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def transferencia_api(request):

    form = TransferenciaForm(request.data)

    if not form.is_valid():
        return Response({
            "status": "erro",
            "codigo": "FORM_INVALIDO",
            "erros": form.errors
        }, status=400)

    agencia = form.cleaned_data["agencia"]
    conta_destino_numero = form.cleaned_data["conta_destino"]
    valor = form.cleaned_data["valor"]
    descricao = form.cleaned_data.get("descricao", "")

    conta_origem = Conta.objects.filter(user=request.user).first()

    if not conta_origem:
        return Response({
            "status": "erro",
            "codigo": "CONTA_ORIGEM_NAO_ENCONTRADA",
            "mensagem": "Conta de origem não encontrada"
        }, status=404)

    try:
        conta_destino = Conta.objects.get(
            numero_conta=conta_destino_numero,
            agencia=agencia
        )
    except Conta.DoesNotExist:
        return Response({
            "status": "erro",
            "codigo": "CONTA_DESTINO_NAO_ENCONTRADA",
            "mensagem": "Conta de destino não encontrada"
        }, status=404)

    if conta_origem.id == conta_destino.id:
        return Response({
            "status": "erro",
            "codigo": "MESMA_CONTA",
            "mensagem": "Não é permitido transferir para a mesma conta"
        }, status=400)

    if valor <= 0:
        return Response({
            "status": "erro",
            "codigo": "VALOR_INVALIDO",
            "mensagem": "O valor da transferência deve ser maior que zero"
        }, status=400)

    if conta_origem.saldo < valor:
        return Response({
            "status": "erro",
            "codigo": "SALDO_INSUFICIENTE",
            "mensagem": "Saldo insuficiente"
        }, status=400)

    try:
        with transaction.atomic():
            conta_origem.saldo -= valor
            conta_origem.save()

            conta_destino.saldo += valor
            conta_destino.save()

            Transacao.objects.create(
                tipo="transferencia",
                conta_origem=conta_origem,
                conta_destino=conta_destino,
                valor=valor,
                descricao=descricao
            )

        return Response({
            "status": "sucesso",
            "codigo": "TRANSFERENCIA_REALIZADA",
            "mensagem": "Transferência realizada com sucesso",
            "saldo_atual": str(conta_origem.saldo)
        }, status=200)

    except Exception:
        return Response({
            "status": "erro",
            "codigo": "ERRO_INTERNO",
            "mensagem": "Erro interno ao processar a transferência"
        }, status=500)
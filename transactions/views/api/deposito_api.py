from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from transactions.forms.deposit_forms import DepositForm
from accounts.models.contas import Conta
from core.models import Transacao

@login_required
def deposito_api(request):
    if request.method != "POST":
        return JsonResponse({
            "status": "erro",
            "codigo": "METODO_INVALIDO",
            "mensagem": "Use POST"
        }, status=405)

    if "valor" not in request.POST:
        return JsonResponse({
            "status": "erro",
            "codigo": "VALOR_NAO_INFORMADO",
            "mensagem": "Informe o valor do depósito"
        }, status=400)

    form = DepositForm(request.POST)

    if not form.is_valid():
        erros = form.errors.get("valor")

        if erros:
            if "maior que zero" in erros[0]:
                return JsonResponse({
                    "status": "erro",
                    "codigo": "VALOR_ZERO_OU_NEGATIVO",
                    "mensagem": "O valor do depósito deve ser maior que zero"
                }, status=400)

        return JsonResponse({
            "status": "erro",
            "codigo": "FORM_INVALIDO",
            "erros": form.errors
        }, status=400)

    valor = form.cleaned_data["valor"]

    conta = Conta.objects.filter(user=request.user).first()
    if not conta:
        return JsonResponse({
            "status": "erro",
            "codigo": "CONTA_NAO_ENCONTRADA",
            "mensagem": "Conta não encontrada"
        }, status=404)

    # Atualiza saldo
    conta.saldo += valor
    conta.save()

    # Registra histórico
    Transacao.objects.create(
        tipo="deposito",
        conta_destino=conta,
        conta_origem=None,
        valor=valor,
        descricao="Depósito via API"
    )

    return JsonResponse({
        "status": "sucesso",
        "codigo": "DEPOSITO_REALIZADO",
        "mensagem": "Depósito realizado com sucesso",
        "novo_saldo": str(conta.saldo)
    })
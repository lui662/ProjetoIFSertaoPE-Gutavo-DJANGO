from django.shortcuts import render
from accounts.models.contas import Conta

def home(request):

    contas_usuario = None
    transacoes = None

    if request.user.is_authenticated:
        contas_usuario = Conta.objects.filter(user=request.user).first()
        if contas_usuario:
            todas_transacoes = contas_usuario.transacoes_origem.all() | contas_usuario.transacoes_destino.all()
            transacoes = todas_transacoes.order_by('-id')[:10]
    context = {
        'conta': contas_usuario,
        'transacoes': transacoes,
    }
    return render(request, 'home.html', context)



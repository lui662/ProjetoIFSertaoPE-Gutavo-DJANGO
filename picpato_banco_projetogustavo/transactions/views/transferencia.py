from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..forms.transferencia_forms import TransferenciaForm
from accounts.models.contas import Conta
from django.db import transaction

from core.models import Transacao

@login_required
def transferencia(request):
    form = TransferenciaForm()

    if request.method == 'POST':
        form = TransferenciaForm(request.POST)

        if form.is_valid():
            agencia_destino = form.cleaned_data['agencia']
            conta_destino_numero = form.cleaned_data['conta_destino']
            valor = form.cleaned_data['valor']
            descricao = form.cleaned_data['descricao']

            conta_origem = Conta.objects.filter(user=request.user).first()

            if not conta_destino_numero:
                messages.error(request, 'Número da conta de destino é obrigatório.')
                return render(request, 'transferir.html', {'form': form})
            
            try:
                consta_destino = Conta.objects.get(numero_conta=conta_destino_numero, agencia=agencia_destino)
            except Conta.DoesNotExist:
                messages.error(request, 'Conta de destino não encontrada.')
                return render(request, 'transferir.html', {'form': form})
            

            if conta_origem == consta_destino:
                messages.error(request, 'Não é possível transferir para a mesma conta.')
                return render(request, 'transferir.html', {'form': form})
            
            if conta_origem.saldo < valor:
                messages.error(request, 'Saldo insuficiente para realizar a transferência.')
                return render(request, 'transferir.html', {'form': form})
            

            try: 
                with transaction.atomic():
                    conta_origem.saldo -= valor
                    conta_origem.save()

                    consta_destino.saldo += valor
                    consta_destino.save()

                    Transacao.objects.create(
                        tipo='transferencia',
                        conta_origem=conta_origem,
                        conta_destino=consta_destino,
                        valor=valor,
                        descricao=descricao
                    )

                    messages.success(request, 'Transferência realizada com sucesso!')
                    return redirect('home')
            
            except Exception as e:
                messages.error(request, f'Erro ao processar a transferência: {str(e)}')
                return redirect('home')
    
    return render(request, 'transferir.html', {'form': form})
    
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms.deposit_forms import DepositForm
from accounts.models.contas import Conta

# CORREÇÃO 1: Importe o nome exato da classe (Maiúsculo)
from core.models import Transacao 

@login_required
def deposito(request):
    if request.method == 'POST':
        
        form = DepositForm(request.POST)
        
        if form.is_valid():
            
            valor = form.cleaned_data['valor']
            # O .first() é ótimo para evitar erros se não achar
            conta = Conta.objects.filter(user=request.user).first()
            
            if conta:
                # 1. Atualiza Saldo
                conta.saldo += valor
                conta.save()
                
                # 2. Cria o Histórico
                Transacao.objects.create(
                    # CORREÇÃO 2: O nome do campo no model é 'tipo', não 'tipo_transacao'
                    tipo='deposito', 
                    conta_destino=conta,
                    conta_origem=None,
                    valor=valor,
                    descricao="Depósito via App" # Adicionei descrição pois o campo existe no model
                )

                messages.success(request, 'Depósito realizado com sucesso!')
                return redirect('home')
            
            else:
                messages.error(request, 'Conta não encontrada.')
        else:
            messages.error(request, 'Formulário inválido. Verifique o valor.')
            
    else:
        form = DepositForm()

    return render(request, 'depositar.html', {'form': form})
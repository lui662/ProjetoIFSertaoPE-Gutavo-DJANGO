from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm # Seu form existente

# --- IMPORTS ADICIONADOS ---
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db import transaction # Para operações atómicas
from django.contrib import messages # Para feedback ao utilizador
from .models import Conta, Transacao # Importamos os modelos
from .forms import DepositoForm 
from django.contrib.auth import logout # <-- 1. IMPORTE O LOGOUT AQUI
# ---------------------------

# --- SUA VIEW DE REGISTO (JÁ EXISTE) ---
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login') 
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# --- SUA HOMEVIEW (JÁ EXISTE) ---
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            conta = self.request.user.conta
            transacoes = conta.transacoes.all().order_by('-data_hora')[:10]
            context['conta'] = conta
            context['transacoes'] = transacoes
        except Conta.DoesNotExist:
            context['conta'] = None
            context['transacoes'] = []
        return context

# --- VIEW DE DEPÓSITO (JÁ EXISTE) ---
@login_required 
@transaction.atomic 
def depositar_view(request):
    
    if request.method == 'POST':
        form = DepositoForm(request.POST)
        
        if form.is_valid():
            valor = form.cleaned_data['valor']
            
            try:
                conta = request.user.conta
                
                conta.saldo += valor
                conta.save()
                
                Transacao.objects.create(
                    conta=conta,
                    tipo='E', 
                    valor=valor,
                    descricao="Depósito (simulado)"
                )
                
                messages.success(request, f"Depósito de R$ {valor} realizado com sucesso!")
                return redirect('home') 
            
            except Conta.DoesNotExist:
                messages.error(request, "Conta não encontrada.")
            except Exception as e:
                messages.error(request, f"Ocorreu um erro inesperado: {e}")
    else:
        form = DepositoForm()

    return render(request, 'depositar.html', {'form': form})

# --- 2. ADICIONE ESTA NOVA FUNÇÃO DE LOGOUT ---
@login_required
def logout_view(request):
    """
    Desloga o utilizador e redireciona para a página de login.
    """
    logout(request)
    messages.success(request, "Você saiu da sua conta com sucesso.")
    return redirect('login') # Redireciona para a página de login
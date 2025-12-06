# PicPato Banco 🏦

> Um simulador de banco digital completo desenvolvido com Python e Django, como parte de um projeto académico.

Este projeto recria as funcionalidades essenciais de um banco digital, incluindo gestão de contas, transações (depósito, transferência) e um fluxo de aprovação de empréstimos. O *front-end* é inspirado no *design* moderno do PicPay.

## 🛠️ Tecnologias Utilizadas

* **Back-end:** Python 3, Django 5
* **Front-end:** HTML5, CSS3 (Design Responsivo)
* **Base de Dados (Dev):** SQLite 3

## ✅ Funcionalidades (Requisitos)

Esta é a lista de requisitos funcionais e o estado atual do projeto:

### Gerais & Autenticação
- [x] Sistema de Registo de Utilizadores
- [x] Sistema de Login e Logout
- [x] Modelo de Utilizador personalizado (`User` com `tipo_usuario`: Cliente/Gerente)
- [x] Redirecionamento da página raiz (`/`) para `/register/`

### Funcionalidades do Cliente
- [x] Criação automática de `Conta` bancária ao registar (via *Signals*)
- [x] **RF003:** Consultar Saldo (na *Home Page*)
- [x] **RF004:** Ver Extrato (últimas 10 transações na *Home Page*)
- [x] **RF006:** Realizar Depósito (simulado)
- [ ] **RF005:** Realizar Transferência (a implementar)
- [ ] **RF007:** Solicitar Empréstimo (a implementar)
- [ ] **RF008:** Ver *status* do Empréstimo (a implementar)

### Funcionalidades do Gerente
- [ ] **RF009:** Login em área administrativa (Django Admin)
- [ ] **RF012:** Visualizar pedidos de empréstimo pendentes (a implementar)
- [ ] **RF013:** Aprovar ou Negar pedidos de empréstimo (a implementar)

## 🚀 Como Executar o Projeto Localmente

Para testar este projeto na sua máquina, siga os passos abaixo:

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
    cd seu-repositorio
    ```

2.  **Crie e ative o Ambiente Virtual (venv):**
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate
    
    # macOS / Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    *(Por agora, apenas o Django)*
    ```bash
    pip install django
    ```

4.  **Aplique as migrações (Crie a base de dados):**
    ```bash
    python manage.py makemigrations core
    python manage.py migrate
    ```

5.  **Execute o servidor:**
    ```bash
    python manage.py runserver
    ```

6.  **Aceda à aplicação:**
    Abra o seu navegador e vá para `http://1227.0.0.1:8000/` (que irá redirecionar para `/register/`).
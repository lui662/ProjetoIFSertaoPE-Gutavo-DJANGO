from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth import login
from accounts.forms.auth.login_forms import CustomUserLoginForms

@csrf_exempt
def login_api(request):
    if request.method == "POST":
        form = CustomUserLoginForms(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return JsonResponse({
                "status": "ok",
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "tipo_usuario": user.tipo_usuario
            }, status=200)

        return JsonResponse({
            "status": "erro",
            "erros": form.errors
        }, status=401)

    return JsonResponse({"erro": "Método inválido"}, status=405)
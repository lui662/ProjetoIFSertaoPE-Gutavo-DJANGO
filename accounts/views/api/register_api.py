from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from accounts.forms.auth.register_forms import CustomUserCreateForms

@csrf_exempt
def register_api(request):
    if request.method == "POST":
        print("POST RAW:", request.POST)

        form = CustomUserCreateForms(request.POST)

        if form.is_valid():
            user = form.save()
            return JsonResponse({
                "status": "ok",
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "tipo_usuario": user.tipo_usuario
            }, status=201)

        print("FORM ERROS:", form.errors)

        return JsonResponse({
            "status": "erro",
            "erros": form.errors
        }, status=400)

    return JsonResponse({"erro": "Método inválido"}, status=405)

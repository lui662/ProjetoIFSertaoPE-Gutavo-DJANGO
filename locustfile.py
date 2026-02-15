from locust import HttpUser, task, between

class UsuarioBanco(HttpUser):

    wait_time = between(1, 5)

    host = "http://127.0.0.1:8000"

    @task(2)
    def acessar_home(self):
        self.client.get("/")

    @task(1)
    def tentar_login(self):
        self.client.post("/login/", {
            "username": "usuario_teste",
            "password": "Teste@123!"
        })
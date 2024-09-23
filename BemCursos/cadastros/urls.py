from django.urls import path
from .views import LoginView, FuncionarioView, home

urlpatterns = [
    path('', home, name='home'),
    path('login', LoginView.as_view(), name='login'),
    path('funcionario', FuncionarioView.as_view(), name='funcionario'),  # Nova rota para a página de funcionários
]

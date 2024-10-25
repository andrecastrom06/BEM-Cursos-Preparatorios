from django.urls import path
from .views import TurmaView, LoginView, home

urlpatterns = [
    path('', home, name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('turmas/', TurmaView.as_view(), name='turmas'),
    path('turmas/adicionar/', TurmaView.as_view(), name='adicionar_turma'),
    path('turmas/<int:turma_id>/', TurmaView.as_view(), name='editar_turma'),
    path('turmas/<int:turma_id>/remover/', TurmaView.as_view(), name='remover_turma'),
]
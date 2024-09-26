from django.urls import path
from .views import LoginView, TurmaView,home
urlpatterns = [
    path('', home, name='home'),
    path('login', LoginView.as_view(), name='login'),
    path('turmas/', TurmaView.as_view(), name='turmas'),  # Listar turmas
    path('turmas/adicionar/', TurmaView.as_view(), name='adicionar_turma'),  # Adicionar turma
    path('turmas/<int:turma_id>/editar/', TurmaView.as_view(), name='editar_turma'),  # Editar turma
    path('turmas/<int:turma_id>/remover/', TurmaView.as_view(), name='remover_turma'),  # Remover turma
    path('alunos', LoginView.as_view(), name='alunos'),
]

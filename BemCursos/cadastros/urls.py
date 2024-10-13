from django.urls import path
from .views import TurmaView, AlunoView, LoginView, ResponsavelView,home

urlpatterns = [
    path('', home, name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('turmas/', TurmaView.as_view(), name='turmas'),
    path('responsavel/', ResponsavelView.as_view(), name='responsavel'),
    path('turmas/adicionar/', TurmaView.as_view(), name='adicionar_turma'),
    path('turmas/<int:turma_id>/', TurmaView.as_view(), name='editar_turma'),
    path('turmas/<int:turma_id>/remover/', TurmaView.as_view(), name='remover_turma'),
    path('turmas/<int:turma_id>/alunos/', AlunoView.as_view(), name='listar_alunos'),
    path('turmas/<int:turma_id>/alunos/adicionar/', AlunoView.as_view(), name='adicionar_aluno'),
    path('turmas/<int:turma_id>/alunos/<int:aluno_id>/editar/', AlunoView.as_view(), name='editar_aluno'),
    path('turmas/<int:turma_id>/alunos/<int:aluno_id>/remover/', AlunoView.as_view(), name='remover_aluno'),
]
from django.urls import path
from .views import TurmaView, LoginView, AlunoView,SimuladoView,NotaView,RankingView, home

urlpatterns = [
    path('', home, name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('turmas/', TurmaView.as_view(), name='turmas'),
    path('turmas/adicionar/', TurmaView.as_view(), name='adicionar_turma'),
    path('turmas/<int:turma_id>/', TurmaView.as_view(), name='editar_turma'),
    path('turmas/<int:turma_id>/remover/', TurmaView.as_view(), name='remover_turma'),
    path('turmas/<int:turma_id>/alunos/', AlunoView.as_view(), name='alunos'),
    path('turmas/<int:turma_id>/alunos/adicionar/', AlunoView.as_view(), name='adicionar_aluno'),
    path('turmas/<int:turma_id>/alunos/<int:aluno_id>/remover/', AlunoView.as_view(), name='remover_aluno'),
    path('simulados/adicionar/', SimuladoView.as_view(), name='adicionar_simulado'),
    path('simulados/<int:simulado_id>/excluir/', SimuladoView.as_view(), name='excluir_simulado'),
    path('simulados/', SimuladoView.as_view(), name='simulados'),
    path('simulado/<int:simulado_id>/notas/', NotaView.as_view(), name='notas_simulado'),
    path('simulado/<int:simulado_id>/ranking/', RankingView.as_view(), name='ranking'),
]



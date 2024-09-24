from django.urls import path
from .views import LoginView, TurmaView,TurmaCreateView,TurmaDeleteView,TurmaEditView ,home
urlpatterns = [
    path('', home, name='home'),
    path('login', LoginView.as_view(), name='login'),
    path('turmas/', TurmaView.as_view(), name='turmas'),  
    path('turmas/adicionar/', TurmaCreateView.as_view(), name='adicionar_turma'), 
    path('turmas/editar/<int:turma_id>/', TurmaEditView.as_view(), name='editar_turma'),  
    path('turmas/remover/<int:turma_id>/', TurmaDeleteView.as_view(), name='remover_turma'),
]

from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from .models import Unidade
from django.contrib import messages
from .mediators import TurmaMediator  # Importando o mediator


# superuser
# username 'bemcursos'
# password 'preparatoriobem'

# Redireciona para a página de login ao acessar a home
def home(request):
    return redirect('login')

class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        # Realiza logout automático quando acessa a página de login
        logout(request)
        return render(request, self.template_name)

    def post(self, request):
        user_type = request.POST.get('user_type')  # Obtém o tipo de usuário
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # Autentica o usuário
            
            # Verifica o tipo de usuário e redireciona para a página apropriada
            if user_type == 'funcionario' and username == 'bemcursos' and password == 'preparatoriobem':
                return redirect('turmas')  # Altere para a URL do painel do funcionário
            
            elif user_type == 'responsavel':
                return redirect('responsavel')  # Altere para a URL do painel do responsável
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
            return render(request, self.template_name)


class TurmaView(LoginRequiredMixin, View):
    login_url = '/login/'
    template_name_list = 'turmas.html'
    template_name_add = 'adicionar_turma.html'

    def get(self, request, turma_id=None):
        if turma_id:
            turma = TurmaMediator.obter_turma(turma_id)
            unidades = Unidade.objects.all()
            return render(request, self.template_name_edit, {'turma': turma, 'unidades': unidades})
        elif request.path.endswith('adicionar/'):
            unidades = Unidade.objects.all()
            return render(request, self.template_name_add, {'unidades': unidades})
        else:
            turmas = TurmaMediator.listar_turmas()
            return render(request, self.template_name_list, {'turmas': turmas})

    def post(self, request):
        if request.POST.get('method') == 'DELETE':
            turma_id = request.POST.get('turma_id')
            try:
                response = TurmaMediator.excluir_turma(turma_id)
                return JsonResponse(response)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)

        nome = request.POST.get('nome')
        unidade_id = request.POST.get('unidade')

        TurmaMediator.adicionar_turma(nome, unidade_id)

        return redirect('turmas')

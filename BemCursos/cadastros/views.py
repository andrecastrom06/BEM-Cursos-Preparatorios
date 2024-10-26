from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from .models import Unidade, Aluno
from django.contrib import messages
from .mediators import TurmaMediator, AlunoMediator
from datetime import datetime

# superuser
# username 'bemcursos'
# password 'preparatoriobem'

# Redireciona para a página de login ao acessar a home
def home(request):
    return redirect('login')

class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        logout(request)
        return render(request, self.template_name)

    def post(self, request):
        user_type = request.POST.get('user_type')  
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
        if request.path.endswith('adicionar/'):
            unidades = Unidade.objects.all()
            return render(request, self.template_name_add, {'unidades': unidades})
        else:
            turmas = TurmaMediator.listar_turmas()
            return render(request, self.template_name_list, {'turmas': turmas})

    def post(self, request, turma_id=None):
        if 'method' in request.POST and request.POST['method'] == 'DELETE':
            if turma_id is not None:
                return self.excluir_turma(turma_id)
            return JsonResponse({'error': 'ID da turma não fornecido'}, status=400)

        nome = request.POST.get('nome')
        unidade_id = request.POST.get('unidade')
        TurmaMediator.adicionar_turma(nome, unidade_id)
        return redirect('turmas')

    def excluir_turma(self, turma_id):
        try:
            response = TurmaMediator.excluir_turma(turma_id)
            return JsonResponse(response)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

class AlunoView(LoginRequiredMixin, View):
    login_url = '/login/'
    template_name_list = 'alunos.html'
    template_name_add = 'adicionar_aluno.html'

    def get(self, request, turma_id=None):
        if request.path.endswith('adicionar/'):
            return render(request, self.template_name_add, {'turma_id': turma_id})
        elif turma_id:
            alunos = AlunoMediator.listar_alunos(turma_id)
            return render(request, self.template_name_list, {'alunos': alunos, 'turma_id': turma_id})
        else:
            return redirect('turmas')

    def post(self, request, turma_id=None):
        if 'remover_aluno_id' in request.POST:
            aluno_id = request.POST.get('remover_aluno_id')
            resultado = AlunoMediator.remover_aluno(aluno_id)
            messages.success(request, resultado['status'])
            return redirect('alunos', turma_id=turma_id)
  
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        cpf = request.POST.get('cpf')
        data_nascimento_str = request.POST.get('data_nascimento')
        data_nascimento = datetime.strptime(data_nascimento_str, "%Y-%m-%d").date()

        aluno_temp = Aluno(nome=nome, sobrenome=sobrenome, cpf=cpf, data_nascimento=data_nascimento, turma_id=turma_id)
        if not aluno_temp.validar_cpf():
            messages.error(request, "CPF inválido. Verifique o número e tente novamente.")
            return render(request, self.template_name_add, {'turma_id': turma_id})

        AlunoMediator.adicionar_aluno(nome, sobrenome, cpf, data_nascimento, turma_id)
        messages.success(request, "Aluno e usuário criados com sucesso!")
        return redirect('alunos', turma_id=turma_id)
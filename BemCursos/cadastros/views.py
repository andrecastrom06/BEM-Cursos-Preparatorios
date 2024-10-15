from django.views import View
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from .models import Aluno, Turma, Unidade
from django.contrib import messages
from django.contrib.auth.models import User


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

# Utiliza LoginRequiredMixin para garantir que apenas usuários autenticados acessem essas views
class TurmaView(LoginRequiredMixin, View):
    login_url = '/login/'  # Redireciona para login se não autenticado
    template_name_list = 'turmas.html'
    template_name_add = 'adicionar_turma.html'
    template_name_edit = 'editar_turma.html'

    # Página de listagem ou adicionar/editar turmas
    def get(self, request, turma_id=None):
        if turma_id:  # Página de editar turma
            turma = get_object_or_404(Turma, id=turma_id)
            unidades = Unidade.objects.all()  # Obtendo todas as unidades
            return render(request, self.template_name_edit, {'turma': turma, 'unidades': unidades})
        elif request.path.endswith('adicionar/'):  # Página de adicionar turma
            unidades = Unidade.objects.all()  # Obtendo todas as unidades
            return render(request, self.template_name_add, {'unidades': unidades})
        else:  # Página de listagem de turmas
            turmas = Turma.objects.all()
            return render(request, self.template_name_list, {'turmas': turmas})

    # Adicionar ou editar turma (POST request)
    def post(self, request, turma_id=None):
        if request.POST.get('method') == 'DELETE':  # Exclusão de turma
            turma_id = request.POST.get('turma_id')
            try:
                turma = get_object_or_404(Turma, id=turma_id)

                # Obter todos os alunos associados à turma
                alunos = Aluno.objects.filter(turma=turma)

                # Excluir todos os alunos e seus usuários
                for aluno in alunos:
                    if aluno.user:  # Verifique se o aluno tem um usuário associado
                        aluno.user.delete()  # Remove o usuário do banco de dados
                    aluno.delete()  # Deleta o aluno

                turma.delete()  # Deleta a turma
                return JsonResponse({'status': 'Turma e alunos removidos com sucesso!'})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)

        # Se não for uma exclusão, trata como adição ou edição de turma
        nome = request.POST.get('nome')
        unidade_id = request.POST.get('unidade')  # Obtenha o ID da unidade
        unidade = get_object_or_404(Unidade, id=unidade_id)  # Busque a unidade

        if turma_id:  # Atualizando turma existente
            turma = get_object_or_404(Turma, id=turma_id)
            turma.nome = nome
            turma.unidade = unidade
            turma.save()
        else:  # Criando nova turma
            Turma.objects.create(nome=nome, unidade=unidade)

        return redirect('turmas')

class AlunoView(TurmaView):  # Herda de TurmaView
    login_url = '/login/'  # Redireciona para login se não autenticado
    template_name_list = 'alunos.html'
    template_name_add = 'adicionar_aluno.html'

    # Exibir lista de alunos ou formulário para adicionar/editar
    def get(self, request, turma_id, aluno_id=None):
        turma = get_object_or_404(Turma, id=turma_id)

        if aluno_id:  # Editar aluno existente
            aluno = get_object_or_404(Aluno, id=aluno_id)
            return render(request, self.template_name_edit, {'turma': turma, 'aluno': aluno})
        elif request.path.endswith('adicionar/'):  # Página para adicionar novo aluno
            return render(request, self.template_name_add, {'turma': turma})
        else:  # Listar alunos da turma
            alunos = Aluno.objects.filter(turma=turma)
            return render(request, self.template_name_list, {'turma': turma, 'alunos': alunos})

    def post(self, request, turma_id, aluno_id=None):
        turma = get_object_or_404(Turma, id=turma_id)

        if request.POST.get('method') == 'DELETE':  # Verifica se a requisição é para deletar
            aluno_id = request.POST.get('aluno_id')  # Obtém o ID do aluno a ser deletado
            aluno = get_object_or_404(Aluno, id=aluno_id)

            # Excluir o usuário associado ao aluno
            if aluno.user:  # Verifique se o aluno tem um usuário associado
                aluno.user.delete()  # Remove o usuário do banco de dados

            aluno.delete()  # Deleta o aluno
            messages.success(request, 'Aluno e usuário removidos com sucesso!')  # Mensagem de sucesso
            return redirect('listar_alunos', turma_id=turma_id)  # Redireciona para a lista de alunos

        # Novo código para adicionar um aluno
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        cpf = request.POST.get('cpf')
        idade = request.POST.get('idade')

        if aluno_id:  # Atualizando aluno existente
            aluno = get_object_or_404(Aluno, id=aluno_id)
            aluno.nome = nome
            aluno.sobrenome = sobrenome
            aluno.cpf = cpf
            aluno.idade = idade
            aluno.turma = turma
            aluno.save()
        else:  # Criando novo aluno
            aluno = Aluno.objects.create(
                nome=nome,
                sobrenome=sobrenome,
                cpf=cpf,
                idade=idade,
                turma=turma
            )
            # Gerar login e senha para o responsável
            username, password = aluno.gerar_login()
            user = User.objects.create_user(username=username, password=password)
            aluno.user = user  # Associar o usuário ao aluno
            aluno.save()  # Salvar as alterações no aluno'

        return redirect('listar_alunos', turma_id=turma_id)

    
class ResponsavelView(LoginRequiredMixin, View):
    login_url = '/login/'  # Redireciona para login se não autenticado
    template_name = 'responsavel.html'

    def get(self, request):
        # Adicionando print para depuração
        print(f"Usuário logado: {request.user.username}")  # Verifique qual usuário está logado
        aluno = get_object_or_404(Aluno, user=request.user)  # Busca pelo aluno relacionado ao usuário logado
        return render(request, self.template_name, {'aluno': aluno})
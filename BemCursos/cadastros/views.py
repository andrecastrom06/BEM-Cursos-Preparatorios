from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from .models import Aluno, Turma
from django.contrib import messages

# superuser
# username 'bemcursos'
# password 'preparatoriobem'

# A home é simples e não precisa de herança, pois só faz um render básico.
def home(request):
    return render(request, 'login.html')

#Herda View, metodo basico do Django
class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == 'bemcursos' and password == 'preparatoriobem':
            return redirect('turmas')  # Redirecionar para página de turmas
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
            return render(request, self.template_name)

# Centralizando todas as operações relacionadas a Turma em uma única classe
# para simplificar o diagrama de classes e facilitar o desenvolvimento.

#Encapsulamento: Os métodos para manipular os dados das turmas estão todos dentro de uma única classe
#organizando melhor o código e mantendo a coesão.

class TurmaView(View):
    template_name_list = 'turmas.html'
    template_name_add = 'adicionar_turma.html'
    template_name_edit = 'editar_turma.html'

    # Listar ou exibir formulário para adicionar/editar turmas
    def get(self, request, turma_id=None):
        if turma_id:  # Página de editar turma
            turma = get_object_or_404(Turma, id=turma_id)
            return render(request, self.template_name_edit, {'turma': turma})
        elif request.path.endswith('adicionar/'):  # Página de adicionar turma
            return render(request, self.template_name_add)
        else:  # Página de listagem de turmas
            turmas = Turma.objects.all()
            return render(request, self.template_name_list, {'turmas': turmas})

    # Adicionar ou editar turma (POST request)
    def post(self, request, turma_id=None):
        # Verifica se é uma requisição de exclusão
        if request.POST.get('method') == 'DELETE':  
            turma_id = request.POST.get('turma_id')
            try:
                turma = get_object_or_404(Turma, id=turma_id)
                turma.delete()
                return JsonResponse({'status': 'Turma removida com sucesso!'})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)  # Retorna um erro em caso de falha

        # Se não for uma requisição de exclusão, trata como adição ou edição
        nome = request.POST.get('nome')
        unidade = request.POST.get('unidade')

        if turma_id:  # Atualizando uma turma existente
            turma = get_object_or_404(Turma, id=turma_id)
            turma.nome = nome
            turma.unidade = unidade
            turma.save()
        else:  # Adicionando uma nova turma
            Turma.objects.create(nome=nome, unidade=unidade)

        # Após adicionar ou editar, redirecionar para a lista de turmas
        return redirect('turmas')
    
class AlunoView(TurmaView):  # Herda de TurmaView
    template_name_list = 'alunos.html'
    template_name_add = 'adicionar_aluno.html'
    template_name_edit = 'editar_aluno.html'

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

    # Adicionar ou editar aluno (POST request)
    def post(self, request, turma_id, aluno_id=None):
        turma = get_object_or_404(Turma, id=turma_id)

        # Verifica se é uma requisição de exclusão
        if request.POST.get('method') == 'DELETE':
            aluno_id = request.POST.get('aluno_id')
            try:
                aluno = get_object_or_404(Aluno, id=aluno_id)
                aluno.delete()
                return JsonResponse({'status': 'Aluno removido com sucesso!'})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)

        # Se não for uma exclusão, trata como adição ou edição de aluno
        nome = request.POST.get('nome')
        idade = request.POST.get('idade')

        if aluno_id:  # Atualizando um aluno existente
            aluno = get_object_or_404(Aluno, id=aluno_id)
            aluno.nome = nome
            aluno.idade = idade
            aluno.turma = turma  # Associa o aluno à turma
            aluno.save()
        else:  # Adicionando um novo aluno
            Aluno.objects.create(nome=nome, idade=idade, turma=turma)
            
        # Após adicionar ou editar, redirecionar para a lista de alunos da turma
        return redirect('listar_alunos', turma_id=turma_id)
from django.views import View
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from .models import Turma
from django.contrib import messages

# superuser
# username 'bemcursos'
# password 'preparatoriobem'
def home(request):
    return render(request, 'login.html')

#utilizando orientação a objeto no login, pois a classe LoginView vai ser herdada de view,
#isso organiza a funcionalidade de login como um objeto, encapsulando o comportamento relacionado ao login dentro dessa classe.

class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        user_type = request.POST.get('user_type')

        if user_type == 'aluno':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirecionar para a página do aluno
            else:
                messages.error(request, 'Credenciais de aluno inválidas.')

        elif user_type == 'funcionario':
            username = request.POST.get('func_username')
            password = request.POST.get('func_password')

            if username == 'bemcursos' and password == 'preparatoriobem':
               
                return redirect('turmas')
            else:
                messages.error(request, 'Credenciais de funcionário inválidas.')

        return render(request, self.template_name)
#Todas as classes (TurmaListView, TurmaCreateView, TurmaEditView, TurmaDeleteView) herdam de View, 
#que é uma classe base fornecida pelo Django.
#A herança permite que suas classes especializadas reutilizem o comportamento definido na classe View, como o gerenciamento de requisições HTTP (GET, POST, etc.).

#O encapsulamento é a prática de agrupar dados e métodos que operam sobre esses dados dentro de uma única unidade.
#  Aqui, os métodos (como get() e post()) são responsáveis por manipular dados das Turmas e estão encapsulados dentro das classes.

#A abstração ocorre na medida em que a complexidade do processamento das requisições HTTP e manipulação do banco de dados é escondida dentro das views.
#O desenvolvedor que utiliza essas classes não precisa saber exatamente como o framework Django lida com as requisições ou como o ORM do Django funciona internamente.

#Polimorfismo refere-se à habilidade de diferentes classes responderem ao mesmo método de maneiras diferentes.
# No contexto dessas views, todas as classes herdam de View e podem implementar seus próprios métodos get() e post() de maneira diferente.

class TurmaView(View):
    template_name_list = 'turmas.html'

    def get(self, request):
        turmas = Turma.objects.all()
        return render(request, self.template_name_list, {'turmas': turmas})

class TurmaCreateView(View):
    template_name_add = 'adicionar_turma.html'

    def get(self, request):
        return render(request, self.template_name_add)

    def post(self, request):
        nome = request.POST.get('nome')
        unidade = request.POST.get('unidade')
        if nome and unidade:
            Turma.objects.create(nome=nome, unidade=unidade)
        return redirect('turmas')

class TurmaEditView(View):
    template_name_edit = 'editar_turma.html'

    def get(self, request, turma_id):
        turma = get_object_or_404(Turma, id=turma_id)
        return render(request, self.template_name_edit, {'turma': turma})

    def post(self, request, turma_id):
        turma = get_object_or_404(Turma, id=turma_id)
        turma.nome = request.POST.get('nome')
        turma.unidade = request.POST.get('unidade')
        turma.save()
        return redirect('turmas')

class TurmaDeleteView(View):
    def post(self, request, turma_id):
        turma = get_object_or_404(Turma, id=turma_id)
        turma.delete()
        return JsonResponse({'status': 'Turma removida com sucesso!'})
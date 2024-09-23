from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
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

            # Verifica as credenciais do funcionário
            if username == 'bemcursos' and password == 'preparatoriobem':
                # Se as credenciais estiverem corretas, redireciona para a página de funcionários
                return redirect('funcionario')  # Redirecione para a URL que corresponde à página de funcionários
            else:
                messages.error(request, 'Credenciais de funcionário inválidas.')

        return render(request, self.template_name)
    
class FuncionarioView(View):
    template_name = 'funcionario.html'

    def get(self, request):
        return render(request, self.template_name)
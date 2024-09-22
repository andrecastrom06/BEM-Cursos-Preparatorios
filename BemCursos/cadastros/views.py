from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

# superuser
# username 'bemcursos'
# password 'preparatoriobem'

def home(request):
    return render(request, "home.html")

def def_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('principal')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    return render(request, 'login.html')

def principal(request):
    return render(request, 'principal.html')
from django.contrib import admin
from .models import Aluno, Turma, Simulado

# Register your models here.
admin.site.register(Aluno)
admin.site.register(Turma)
admin.site.register(Simulado)
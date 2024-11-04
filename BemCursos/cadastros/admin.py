from django.contrib import admin
from .models import Turma, Unidade, Aluno, Nota, Simulado

admin.site.register(Turma)
admin.site.register(Unidade)
admin.site.register(Aluno)
admin.site.register(Nota)
admin.site.register(Simulado)
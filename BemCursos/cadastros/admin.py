from django.contrib import admin
from .models import Aluno, Turma, Simulado, Unidade

# Register your models here.
admin.site.register(Aluno)
admin.site.register(Turma)
admin.site.register(Simulado)
admin.site.register(Unidade)

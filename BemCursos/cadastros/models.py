from django.db import models
from django.contrib.auth.models import User

class Turma(models.Model):
    nome = models.CharField(max_length=100)
    unidade = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.nome} - {self.unidade}'

class Aluno(models.Model):
    nome = models.CharField(max_length=30)
    sobrenome = models.CharField(max_length=30)   
    cpf = models.CharField(max_length=11, unique=True)  
    idade = models.IntegerField()
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='alunos')
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='aluno')  

    def __str__(self):
        return f'{self.nome} {self.sobrenome}'

    def gerar_login(self):
        username = f"{self.nome.lower()}{self.sobrenome.lower()}{self.turma.nome.lower()}"
        password = self.cpf
        return username, password

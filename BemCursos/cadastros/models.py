from django.db import models
from django.contrib.auth.models import User

class Unidade(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome

class Turma(models.Model):
    nome = models.CharField(max_length=100)
    unidade = models.ForeignKey(Unidade, on_delete=models.CASCADE, related_name='turmas')

    def __str__(self):
        return f'{self.nome} - {self.unidade.nome}'

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
        # Remove espaços nos nomes, sobrenome e turma
        username = f"{self.nome.replace(' ', '').lower()}{self.sobrenome.replace(' ', '').lower()}{self.turma.nome.replace(' ', '').lower()}"
        password = self.cpf
        return username, password

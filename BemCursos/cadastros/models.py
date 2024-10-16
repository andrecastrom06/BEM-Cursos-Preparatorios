from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

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
    data_nascimento = models.DateField(blank=True,null=True) # Novo campo para data de nascimento #O usuário vai inserir a data de nascimento e o programa irá calcular a idade
    idade = models.IntegerField(null=True,blank=True)  # Você pode calcular a idade a partir da data de nascimento
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='alunos')
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='aluno')  

    def idade_em_dias(self):
        """Calcula a idade do aluno em dias."""
        if self.data_nascimento:
            idade = (timezone.now().date() - self.data_nascimento).days
            return idade
    def __str__(self):
        return f'{self.nome} {self.sobrenome}'

    def gerar_login(self):
        # Remove espaços nos nomes, sobrenome e turma
        username = f"{self.nome.replace(' ', '').lower()}{self.sobrenome.replace(' ', '').lower()}{self.turma.nome.replace(' ', '').lower()}"
        password = self.cpf
        return username, password
    
class Simulado(models.Model):
    nome = models.CharField(max_length=100)
    turmas = models.ManyToManyField(Turma, related_name='simulados')  
    data = models.DateField()

    def __str__(self):
        return f"{self.nome} - {self.data}"
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
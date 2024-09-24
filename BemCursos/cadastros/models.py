from django.db import models

from django.db import models

class Turma(models.Model):
    nome = models.CharField(max_length=100)
    unidade = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.nome} - {self.unidade}'


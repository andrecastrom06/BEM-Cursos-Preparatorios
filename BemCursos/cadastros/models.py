from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime

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
    nome = models.CharField(max_length=50)
    sobrenome = models.CharField(max_length=50)
    cpf = models.CharField(max_length=11, unique=True)
    data_nascimento = models.DateField()
    idade_em_dias = models.PositiveIntegerField(editable=False)

    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='alunos')

    def __str__(self):
        return f'{self.nome} {self.sobrenome}'

    def calcular_idade_em_dias(self):
        """Calcula a idade do aluno em dias com base na data de nascimento."""
        hoje = timezone.now().date()
        idade_dias = (hoje - self.data_nascimento).days
        self.idade_em_dias = idade_dias
        return idade_dias

    def validar_cpf(self):
        """Valida o CPF, retornando True se o CPF for válido, ou False se não for."""
        cpf = self.cpf
        if not cpf.isdigit() or len(cpf) != 11 or len(set(cpf)) == 1:
            return False

        def calcular_digito(digitos):
            soma = sum((len(digitos) + 1 - i) * int(num) for i, num in enumerate(digitos))
            resto = soma % 11
            return 0 if resto < 2 else 11 - resto

        digito1 = calcular_digito(cpf[:9])
        digito2 = calcular_digito(cpf[:10])
        return cpf[-2:] == f"{digito1}{digito2}"

    def save(self, *args, **kwargs):
        self.calcular_idade_em_dias()
        super().save(*args, **kwargs)

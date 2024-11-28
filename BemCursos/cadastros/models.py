from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
import unicodedata

class Unidade(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.nome

class Turma(models.Model):
    nome = models.CharField(max_length=100)
    unidade = models.ForeignKey(Unidade, on_delete=models.CASCADE, related_name='turmas')

    def __str__(self):
        return f'{self.nome} - {self.unidade.nome}'
    
#def usada no login para remover possiveis acentos gráficos nos nomes
def remover_acentos(texto):
    return ''.join(char for char in unicodedata.normalize('NFD', texto)if unicodedata.category(char) != 'Mn')


class Aluno(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    nome = models.CharField(max_length=50)
    sobrenome = models.CharField(max_length=50)
    cpf = models.CharField(max_length=11, unique=True)
    data_nascimento = models.DateField()
    idade_em_dias = models.PositiveIntegerField(editable=False)
    turma = models.ForeignKey('Turma', on_delete=models.CASCADE, related_name='alunos')
    is_ver_geral = models.BooleanField(default=False, verbose_name="Permissão para Visualizar Ranking Geral")

    def __str__(self):
        return f'{self.nome} {self.sobrenome}'

    def calcular_idade_em_dias(self):
        hoje = timezone.now().date()
        idade_dias = (hoje - self.data_nascimento).days
        self.idade_em_dias = idade_dias
        return idade_dias

    def validar_cpf(self):
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

    def gerar_login(self):
        texto =  f"{self.nome}{self.sobrenome}{self.turma.nome}".lower().strip().replace(' ', '')
        return remover_acentos(texto)

    def gerar_senha(self):
        return self.cpf

    def save(self, *args, **kwargs):
        self.calcular_idade_em_dias()

        if not self.user_id:
            login = self.gerar_login()
            senha = self.gerar_senha()

            if User.objects.filter(username=login).exists():
                raise ValidationError(f"O nome de usuário '{login}' já existe.")

            user = User.objects.create_user(username=login, password=senha)
            self.user = user

        super().save(*args, **kwargs)

class Simulado(models.Model):
    TIPOS_SIMULADO = [
        ('CM', 'Colégio Militar'),
        ('EA', 'Escola de Aplicação'),
    ]
    
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=2, choices=TIPOS_SIMULADO)
    data = models.DateField()

    def __str__(self):
        return f"{self.nome} ({self.get_tipo_display()}) - {self.data}"
    
    def registrar_notas(self, notas_alunos):
        """Registra as notas de todos os alunos no simulado."""
        for aluno, notas in notas_alunos.items():
            Nota.objects.update_or_create(
                aluno=aluno,
                simulado=self,
                defaults={
                    'nota_mat': notas.get('mat', None),
                    'nota_port': notas.get('port', None),
                }
            )

    def calcular_resultados(self):
        notas = self.nota_set.all()
        return sorted(
            notas,
            key=lambda nota: (nota.nota_final, nota.aluno.idade_em_dias),
            reverse=True
        )

class Nota(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)  
    simulado = models.ForeignKey(Simulado, on_delete=models.CASCADE)  
    matematica_acertos = models.IntegerField(default=0)
    portugues_acertos = models.IntegerField(default=0)
    
    @property
    def nota_final(self):
        if self.simulado.tipo == "Colégio Militar": 
            return (self.acertos_mat + self.acertos_port) / 2  
        elif self.simulado.tipo == "Escola de Aplicação":
            return self.acertos_mat + self.acertos_port  
        return 0

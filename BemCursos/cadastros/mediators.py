from django.shortcuts import get_object_or_404
from .models import Turma, Unidade, Aluno

class TurmaMediator:
    @staticmethod
    def listar_turmas():
        return Turma.objects.all()

    @staticmethod
    def obter_turma(turma_id):
        return get_object_or_404(Turma, id=turma_id)

    @staticmethod
    def adicionar_turma(nome, unidade_id):
        unidade = get_object_or_404(Unidade, id=unidade_id)
        Turma.objects.create(nome=nome, unidade=unidade)

    @staticmethod
    def excluir_turma(turma_id):
        turma = get_object_or_404(Turma, id=turma_id)
        turma.delete()
        return {'status': 'Turma removida com sucesso!'}
    

class AlunoMediator:
    @staticmethod
    def listar_alunos(turma_id):
        return Aluno.objects.filter(turma__id=turma_id)

    @staticmethod
    def adicionar_aluno(nome, sobrenome, cpf, data_nascimento, turma_id):
        turma = Turma.objects.get(id=turma_id)
        aluno = Aluno(
            nome=nome,
            sobrenome=sobrenome,
            cpf=cpf,
            data_nascimento=data_nascimento,
            turma=turma
        )
        aluno.calcular_idade_em_dias()
        aluno.save()

    @staticmethod
    def remover_aluno(aluno_id):
        aluno = get_object_or_404(Aluno, id=aluno_id)
        aluno.delete()
        return {'status': 'Aluno removido com sucesso!'}

from django.shortcuts import get_object_or_404
from .models import Turma, Unidade, Aluno, Simulado, User

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
        
        alunos = Aluno.objects.filter(turma=turma)
        for aluno in alunos:
            login = aluno.gerar_login()  
            usuario = User.objects.filter(username=login).first()
            if usuario:
                usuario.delete()  
            aluno.delete()  

        turma.delete()
        return {'status': 'Turma, alunos e usuários removidos com sucesso!'}

class AlunoMediator:
    @staticmethod
    def listar_alunos(turma_id):
        return Aluno.objects.filter(turma__id=turma_id)

    @staticmethod
    def adicionar_aluno(nome, sobrenome, cpf, data_nascimento, turma_id):
        turma = get_object_or_404(Turma, id=turma_id)
        
        aluno = Aluno(
            nome=nome,
            sobrenome=sobrenome,
            cpf=cpf,
            data_nascimento=data_nascimento,
            turma=turma
        )
        aluno.calcular_idade_em_dias()
        aluno.save()

        login = aluno.gerar_login()
        senha = aluno.gerar_senha()

        if not User.objects.filter(username=login).exists():
            User.objects.create_user(
                username=login,
                password=senha
            )

    @staticmethod
    def remover_aluno(aluno_id):
        aluno = get_object_or_404(Aluno, id=aluno_id)
        
        login = aluno.gerar_login()
        usuario = User.objects.filter(username=login).first()
        if usuario:
            usuario.delete()

        aluno.delete()
        return {'status': 'Aluno e usuário removidos com sucesso!'}


class SimuladoMediator:
    @staticmethod
    def listar_simulados():
        return Simulado.objects.all()

    @staticmethod
    def adicionar_simulado(nome, tipo, data):
        if not nome or not tipo or not data:
            raise ValueError("Todos os campos são obrigatórios!")
        Simulado.objects.create(nome=nome, tipo=tipo, data=data)

    @staticmethod
    def excluir_simulado(simulado_id):
        simulado = get_object_or_404(Simulado, id=simulado_id)
        simulado.delete()
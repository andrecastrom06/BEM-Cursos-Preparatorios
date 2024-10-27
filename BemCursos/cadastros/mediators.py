from django.shortcuts import get_object_or_404
from .models import Turma, Unidade, Aluno, Simulado,Nota, User
from django.db import transaction
from django.db.models import Avg, F

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
        
        # Cria o aluno temporariamente para gerar login e senha
        aluno = Aluno(
            nome=nome,
            sobrenome=sobrenome,
            cpf=cpf,
            data_nascimento=data_nascimento,
            turma=turma
        )
        aluno.calcular_idade_em_dias()
        
        # Gera o login e a senha
        login = aluno.gerar_login()
        senha = aluno.gerar_senha()

        # Cria o usuário e o associa ao aluno
        usuario = User.objects.create_user(
            username=login,
            password=senha
        )
        aluno.user = usuario
        aluno.save()  # Salva o aluno com o usuário associado

    @staticmethod
    def remover_aluno(aluno_id):
        aluno = get_object_or_404(Aluno, id=aluno_id)
        aluno.delete()  
        aluno.user.delete()
        return {'status': 'Aluno e usuário removidos com sucesso!'}


class SimuladoMediator:
    @staticmethod
    def listar_simulados():
        return Simulado.objects.all()

    @staticmethod
    def adicionar_simulado(nome, tipo, data):
        return Simulado.objects.create(nome=nome, tipo=tipo, data=data)

    @staticmethod
    def excluir_simulado(simulado_id):
        simulado = Simulado.objects.get(id=simulado_id)
        simulado.delete()


class NotaMediator:
    @staticmethod
    def obter_alunos():
        return Aluno.objects.all()

    @staticmethod
    def salvar_notas(simulado_id, request):
        simulado = Simulado.objects.get(id=simulado_id)

        with transaction.atomic():
            for aluno in Aluno.objects.all():
                matematica_acertos = request.POST.get(f'matematica_{aluno.id}')
                portugues_acertos = request.POST.get(f'portugues_{aluno.id}')

                if matematica_acertos is not None:
                    Nota.objects.update_or_create(
                        aluno=aluno,
                        simulado=simulado,
                        defaults={'matematica_acertos': int(matematica_acertos)}
                    )
                if portugues_acertos is not None:
                    Nota.objects.update_or_create(
                        aluno=aluno,
                        simulado=simulado,
                        defaults={'portugues_acertos': int(portugues_acertos)}
                    )


class RankingMediator:
    @staticmethod
    def calcular_rankings(simulado):
        tipo_simulado = simulado.tipo
        
        if tipo_simulado == 'CM':  # Colégio Militar
            rankings = (
                Nota.objects.filter(simulado=simulado)
                .values('aluno__nome', 'aluno__sobrenome', 'aluno__idade_em_dias', 'aluno__data_nascimento')
                .annotate(
                    media_matematica=Avg(F('matematica_acertos') * 0.5),
                    media_portugues=Avg(F('portugues_acertos') * 0.5),
                    media_final=(F('media_matematica') + F('media_portugues')) / 2
                )
            )
        
        elif tipo_simulado == 'EA':  # Escola de Aplicação
            rankings = (
                Nota.objects.filter(simulado=simulado)
                .values('aluno__nome', 'aluno__sobrenome', 'aluno__idade_em_dias', 'aluno__data_nascimento')
                .annotate(
                    media_matematica=Avg(F('matematica_acertos')),
                    media_portugues=Avg(F('portugues_acertos')),
                    media_final=(F('media_matematica') + F('media_portugues'))
                )
            )
        
        return rankings.order_by('-media_final', '-media_matematica', '-aluno__idade_em_dias')

    @staticmethod
    def calcular_ranking_matematica(simulado):
        rankings = (
            Nota.objects.filter(simulado=simulado)
            .values('aluno__nome', 'aluno__sobrenome', 'aluno__idade_em_dias', 'aluno__data_nascimento')
            .annotate(media_matematica=Avg(F('matematica_acertos') * 0.5))
            .order_by('-media_matematica', '-aluno__idade_em_dias')
        )
        
        return rankings

    @staticmethod
    def calcular_ranking_portugues(simulado):
        rankings = (
            Nota.objects.filter(simulado=simulado)
            .values('aluno__nome', 'aluno__sobrenome', 'aluno__idade_em_dias', 'aluno__data_nascimento')
            .annotate(media_portugues=Avg(F('portugues_acertos') * 0.5))
            .order_by('-media_portugues', '-aluno__idade_em_dias')
        )
        
        return rankings

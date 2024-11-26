from django.shortcuts import get_object_or_404
from .models import Turma, Unidade, Aluno, Simulado,Nota, User
from django.db import transaction
from django.db.models import Avg, F, FloatField, IntegerField,Q
from django.db.models.functions import Cast


class TurmaMediator:
    @staticmethod
    def obter_turmas():
        return Turma.objects.all()
    
    @staticmethod
    def listar_turmas():
        return Turma.objects.all().order_by("nome")

    @staticmethod
    def listar_turmas_por_unidade(unidade_id):
        return Turma.objects.filter(unidade_id=unidade_id).order_by("nome")

    @staticmethod
    def obter_turma(turma_id):
        return get_object_or_404(Turma, id=turma_id)

    @staticmethod
    def adicionar_turma(nome, unidade_id):
        unidade = get_object_or_404(Unidade, id=unidade_id)
        nome_formatado = nome.strip().capitalize()
        Turma.objects.create(nome=nome_formatado, unidade=unidade)

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

    @staticmethod
    def listar_unidades():
        return Unidade.objects.all()


class AlunoMediator:
    @staticmethod
    def listar_alunos(turma_id):
        return Aluno.objects.filter(turma__id=turma_id)
    
    @staticmethod
    def obter_aluno(user):
        return get_object_or_404(Aluno, user=user)
    
    @staticmethod
    def adicionar_aluno(nome, sobrenome, cpf, data_nascimento, turma_id, is_ver_geral):
        turma = get_object_or_404(Turma, id=turma_id)

        # Normalizar nome e sobrenome (primeira letra maiúscula)
        nome = nome.strip().capitalize()
        sobrenome = sobrenome.strip().title()

        # Verificação de duplicatas
        if Aluno.objects.filter(nome=nome, sobrenome=sobrenome).exists():
            raise ValueError(f"Já existe um aluno cadastrado com o nome {nome} {sobrenome}.")
        if Aluno.objects.filter(cpf=cpf).exists():
            raise ValueError("Já existe um aluno cadastrado com este CPF.")

        aluno = Aluno(
            nome=nome,
            sobrenome=sobrenome,
            cpf=cpf,
            data_nascimento=data_nascimento,
            turma=turma,
            is_ver_geral=is_ver_geral
        )
        aluno.calcular_idade_em_dias()

        login = aluno.gerar_login()
        senha = aluno.gerar_senha()

        usuario = User.objects.create_user(
            username=login,
            password=senha
        )
        aluno.user = usuario
        aluno.save()

    @staticmethod
    def remover_aluno(aluno_id):
        aluno = get_object_or_404(Aluno, id=aluno_id)
        aluno.delete()
        aluno.user.delete()
        return {'status': 'Aluno e usuário removidos com sucesso!'}




class SimuladoMediator:

    @staticmethod
    def obter_simulado(simulado_id):
        return get_object_or_404(Simulado, id=simulado_id)
    
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
        return Aluno.objects.all().order_by('nome','sobrenome')

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
    def _calcular_medias(queryset, tipo_simulado):
        if tipo_simulado == 'CM':
            return queryset.annotate(
                media_matematica=Cast(Avg(F('matematica_acertos') * 0.5), FloatField()),
                media_portugues=Cast(Avg(F('portugues_acertos') * 0.5), FloatField()),
                media_final=Cast((F('media_matematica') / 2 + F('media_portugues') / 2), FloatField())
            )
        elif tipo_simulado == 'EA':
            return queryset.annotate(
                media_matematica=Cast(Avg(F('matematica_acertos')), IntegerField()),
                media_portugues=Cast(Avg(F('portugues_acertos')), IntegerField()),
                media_final=Cast((F('media_matematica') + F('media_portugues')), IntegerField())
            )
        return queryset

    @staticmethod
    def calcular_rankings(simulado):
        tipo_simulado = simulado.tipo
        rankings = (
            Nota.objects.filter(simulado=simulado)
            .values(
                'aluno__id', 'aluno__nome', 'aluno__sobrenome', 
                'aluno__idade_em_dias', 'aluno__data_nascimento', 'aluno__turma__nome'
            )
        )
        rankings = RankingMediator._calcular_medias(rankings, tipo_simulado)

        ordered_rankings = rankings.order_by('-media_final', '-media_matematica', '-aluno__idade_em_dias')
        for posicao, aluno in enumerate(ordered_rankings, start=1):
            aluno['posicao'] = posicao

        return ordered_rankings

    @staticmethod
    def calcular_ranking_matematica(simulado):
        tipo_simulado = simulado.tipo
        rankings = (
            Nota.objects.filter(simulado=simulado)
            .values(
                'aluno__id', 'aluno__nome', 'aluno__sobrenome', 
                'aluno__idade_em_dias', 'aluno__data_nascimento', 'aluno__turma__nome'
            )
        )
        rankings = RankingMediator._calcular_medias(rankings, tipo_simulado)

        ordered_rankings = rankings.order_by('-media_matematica', '-aluno__idade_em_dias')
        for posicao, aluno in enumerate(ordered_rankings, start=1):
            aluno['posicao'] = posicao

        return ordered_rankings

    @staticmethod
    def calcular_ranking_portugues(simulado):
        tipo_simulado = simulado.tipo
        rankings = (
            Nota.objects.filter(simulado=simulado)
            .values(
                'aluno__id', 'aluno__nome', 'aluno__sobrenome', 
                'aluno__idade_em_dias', 'aluno__data_nascimento', 'aluno__turma__nome'
            )
        )
        rankings = RankingMediator._calcular_medias(rankings, tipo_simulado)
        ordered_rankings = rankings.order_by('-media_portugues', '-aluno__idade_em_dias')
        for posicao, aluno in enumerate(ordered_rankings, start=1):
            aluno['posicao'] = posicao

        return ordered_rankings

    @staticmethod
    def calcular_rankingTurma(simulado, turma_id):
        tipo_simulado = simulado.tipo
        notas_turma = Nota.objects.filter(simulado=simulado, aluno__turma_id=turma_id)
        rankings = (
            notas_turma
            .values(
                'aluno__id', 'aluno__nome', 'aluno__sobrenome', 
                'aluno__idade_em_dias', 'aluno__data_nascimento', 'aluno__turma__nome'
            )
        )
        rankings = RankingMediator._calcular_medias(rankings, tipo_simulado)
        ordered_rankings = rankings.order_by('-media_final', '-media_matematica', '-aluno__idade_em_dias')
        for posicao, aluno in enumerate(ordered_rankings, start=1):
            aluno['posicao'] = posicao

        return list(ordered_rankings) 


class RankingResponsavelMediator:
    @staticmethod
    def calcular_rankings_gerais(simulado):
        tipo_simulado = simulado.tipo
        rankings = Nota.objects.filter(simulado=simulado).values(
            'aluno__id', 'aluno__nome', 'aluno__sobrenome', 
            'aluno__idade_em_dias', 'aluno__data_nascimento', 
            'aluno__turma__nome'
        )
        rankings = RankingMediator._calcular_medias(rankings, tipo_simulado)
        ordered_rankings = rankings.order_by('-media_final', '-media_matematica', '-aluno__idade_em_dias')
        for posicao, aluno in enumerate(ordered_rankings, start=1):
            aluno['posicao'] = posicao

        return list(ordered_rankings)

    @staticmethod
    def calcular_rankings_turma(simulado, turma_id):
        rankings = Nota.objects.filter(simulado=simulado, aluno__turma_id=turma_id).values(
            'aluno__id', 'aluno__nome', 'aluno__sobrenome', 
            'aluno__idade_em_dias', 'aluno__data_nascimento', 
            'aluno__turma__nome'
        )
        rankings = RankingMediator._calcular_medias(rankings, simulado.tipo)

        ordered_rankings = rankings.order_by('-media_final', '-media_matematica', '-aluno__idade_em_dias')
        for posicao, aluno in enumerate(ordered_rankings, start=1):
            aluno['posicao'] = posicao

        return list(ordered_rankings)

    @staticmethod
    def calcular_ranking_aluno(simulado, aluno_id):
        tipo_simulado = simulado.tipo
        rankings = Nota.objects.filter(simulado=simulado).values(
            'aluno__id', 'aluno__nome', 'aluno__sobrenome', 
            'aluno__idade_em_dias', 'aluno__data_nascimento', 
            'aluno__turma__nome'
        )
        rankings = RankingMediator._calcular_medias(rankings, tipo_simulado)

        ordered_rankings = rankings.order_by('-media_final', '-media_matematica', '-aluno__idade_em_dias')
        for posicao, aluno in enumerate(ordered_rankings, start=1):
            if aluno['aluno__id'] == aluno_id:
                aluno['posicao'] = posicao
                return aluno

        return None

    @staticmethod
    def calcular_ranking_aluno_turma(simulado, aluno_id, turma_id):
        rankings = Nota.objects.filter(simulado=simulado, aluno__turma_id=turma_id).values(
            'aluno__id', 'aluno__nome', 'aluno__sobrenome', 
            'aluno__idade_em_dias', 'aluno__data_nascimento', 
            'aluno__turma__nome'
        )
        rankings = RankingMediator._calcular_medias(rankings, simulado.tipo)

        ordered_rankings = rankings.order_by('-media_final', '-media_matematica', '-aluno__idade_em_dias')
        for posicao, aluno in enumerate(ordered_rankings, start=1):
            if aluno['aluno__id'] == aluno_id:
                aluno['posicao'] = posicao
                return aluno
        return None

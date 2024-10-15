from django.core.management.base import BaseCommand
from cadastros.models import Unidade

class Command(BaseCommand):
    help = 'Cria unidades predefinidas'
    def handle(self, *args, **kwargs):
        unidades = ['Casa Forte', 'Olinda', 'Boa Viagem']
        for unidade in unidades:
            Unidade.objects.get_or_create(nome=unidade)
            self.stdout.write(self.style.SUCCESS(f'Unidade "{unidade}" criada.'))

#Comando personalizado: python manage.py create_unidades
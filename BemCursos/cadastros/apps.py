from django.apps import AppConfig


class CadastrosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cadastros'
    
    def ready(self):
        from .models import Unidade

        # Cria unidades predefinidas
        Unidade.objects.get_or_create(nome='Casa Forte')
        Unidade.objects.get_or_create(nome='Olinda')
        Unidade.objects.get_or_create(nome='Boa Viagem')

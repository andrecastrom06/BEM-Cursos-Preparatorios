# Generated by Django 5.1.2 on 2024-10-25 19:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0005_simulado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='simulado',
            name='turmas',
        ),
        migrations.DeleteModel(
            name='Aluno',
        ),
        migrations.DeleteModel(
            name='Simulado',
        ),
    ]
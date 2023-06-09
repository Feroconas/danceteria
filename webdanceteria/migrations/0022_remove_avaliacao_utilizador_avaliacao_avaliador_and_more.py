# Generated by Django 4.2.1 on 2023-05-14 17:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('webdanceteria', '0021_alter_auladanca_nome_alter_diretor_descricao_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='avaliacao',
            name='utilizador',
        ),
        migrations.AddField(
            model_name='avaliacao',
            name='avaliador',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='avaliacao',
            name='evento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webdanceteria.evento'),
        ),
    ]

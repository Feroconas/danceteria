# Generated by Django 4.1.7 on 2023-05-13 13:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('webdanceteria', '0015_alter_diretor_imagem_perfil_alter_evento_imagem_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bilheteaula',
            name='aula',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webdanceteria.auladanca'),
        ),
        migrations.AlterField(
            model_name='bilheteaula',
            name='comprador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='bilheteevento',
            name='comprador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='bilheteevento',
            name='evento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webdanceteria.evento'),
        ),
    ]

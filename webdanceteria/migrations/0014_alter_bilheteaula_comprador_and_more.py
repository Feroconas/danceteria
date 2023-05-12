# Generated by Django 4.1.7 on 2023-05-12 15:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webdanceteria', '0013_alter_evento_imagem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bilheteaula',
            name='comprador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='webdanceteria.membro'),
        ),
        migrations.AlterField(
            model_name='bilheteevento',
            name='comprador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='webdanceteria.membro'),
        ),
        migrations.AlterField(
            model_name='diretor',
            name='imagem_perfil',
            field=models.FileField(null=True, upload_to='webdanceteria/static/webdanceteria/media/utilizadorImg'),
        ),
        migrations.AlterField(
            model_name='evento',
            name='imagem',
            field=models.FileField(null=True, upload_to='webdanceteria/static/webdanceteria/media/eventoImg'),
        ),
        migrations.AlterField(
            model_name='instrutor',
            name='imagem_perfil',
            field=models.FileField(null=True, upload_to='webdanceteria/static/webdanceteria/media/utilizadorImg'),
        ),
        migrations.AlterField(
            model_name='membro',
            name='imagem_perfil',
            field=models.FileField(null=True, upload_to='webdanceteria/static/webdanceteria/media/utilizadorImg'),
        ),
    ]
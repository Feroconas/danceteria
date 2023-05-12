# Generated by Django 4.1.7 on 2023-05-12 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webdanceteria', '0014_alter_bilheteaula_comprador_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diretor',
            name='imagem_perfil',
            field=models.FileField(null=True, upload_to='utilizadorImg'),
        ),
        migrations.AlterField(
            model_name='evento',
            name='imagem',
            field=models.FileField(null=True, upload_to='eventoImg'),
        ),
        migrations.AlterField(
            model_name='instrutor',
            name='imagem_perfil',
            field=models.FileField(null=True, upload_to='utilizadorImg'),
        ),
        migrations.AlterField(
            model_name='membro',
            name='imagem_perfil',
            field=models.FileField(null=True, upload_to='utilizadorImg'),
        ),
    ]

# Generated by Django 4.1.7 on 2023-05-12 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webdanceteria', '0011_alter_diretor_imagem_perfil_alter_evento_imagem_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diretor',
            name='imagem_perfil',
            field=models.FileField(null=True, upload_to='webdanceteria/static/webdanceteria/utilizadorImg'),
        ),
        migrations.AlterField(
            model_name='instrutor',
            name='imagem_perfil',
            field=models.FileField(null=True, upload_to='webdanceteria/static/webdanceteria/utilizadorImg'),
        ),
        migrations.AlterField(
            model_name='membro',
            name='imagem_perfil',
            field=models.FileField(null=True, upload_to='webdanceteria/static/webdanceteria/utilizadorImg'),
        ),
    ]
# Generated by Django 4.1.7 on 2023-05-12 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webdanceteria', '0010_alter_auladanca_nivel_aconselhado_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diretor',
            name='imagem_perfil',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='evento',
            name='imagem',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='instrutor',
            name='imagem_perfil',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='membro',
            name='imagem_perfil',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]

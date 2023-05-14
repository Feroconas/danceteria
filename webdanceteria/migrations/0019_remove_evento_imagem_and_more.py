# Generated by Django 4.2.1 on 2023-05-14 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webdanceteria', '0018_remove_nivelmembro_especial_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='evento',
            name='imagem',
        ),
        migrations.AlterField(
            model_name='auladanca',
            name='nivel_aconselhado',
            field=models.IntegerField(choices=[(1, 'Novato'), (2, 'Iniciante'), (3, 'Intermédio'), (4, 'Avançado'), (5, 'Profissional')]),
        ),
        migrations.AlterField(
            model_name='nivelmembro',
            name='id_nivel',
            field=models.IntegerField(choices=[(1, 'Novato'), (2, 'Iniciante'), (3, 'Intermédio'), (4, 'Avançado'), (5, 'Profissional')], primary_key=True, serialize=False),
        ),
    ]
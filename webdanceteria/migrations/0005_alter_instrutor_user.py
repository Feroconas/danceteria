# Generated by Django 4.2 on 2023-05-09 14:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('webdanceteria', '0004_alter_instrutor_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instrutor',
            name='user',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

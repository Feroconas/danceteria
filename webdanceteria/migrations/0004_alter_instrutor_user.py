# Generated by Django 4.2 on 2023-05-09 14:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('webdanceteria', '0003_alter_nivelmembro_id_nivel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instrutor',
            name='user',
            field=models.OneToOneField(default=None, editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

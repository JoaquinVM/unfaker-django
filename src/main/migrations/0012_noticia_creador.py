# Generated by Django 3.0.4 on 2020-03-25 21:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20200325_1653'),
    ]

    operations = [
        migrations.AddField(
            model_name='noticia',
            name='creador',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]

# Generated by Django 3.0.4 on 2020-03-23 23:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20200323_1909'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='denuncia',
            name='fecha',
        ),
    ]

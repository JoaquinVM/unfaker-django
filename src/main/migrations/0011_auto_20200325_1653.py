# Generated by Django 3.0.4 on 2020-03-25 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_auto_20200324_0924'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='noticia',
            name='creador',
        ),
        migrations.AlterField(
            model_name='noticia',
            name='descripcion',
            field=models.CharField(max_length=2000),
        ),
    ]

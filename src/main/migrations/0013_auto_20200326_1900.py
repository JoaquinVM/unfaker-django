# Generated by Django 3.0.4 on 2020-03-26 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_noticia_creador'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noticia',
            name='descripcion',
            field=models.CharField(max_length=100000),
        ),
    ]

# Generated by Django 3.0.4 on 2020-03-26 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_auto_20200326_1900'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noticia',
            name='descripcion',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='noticia',
            name='titulo',
            field=models.TextField(),
        ),
    ]
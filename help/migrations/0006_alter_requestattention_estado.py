# Generated by Django 4.2 on 2024-04-01 01:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('help', '0005_alter_requestattention_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestattention',
            name='estado',
            field=models.CharField(blank=True, choices=[('pendiente', 'Pendiente'), ('en proceso', 'En proceso'), ('finalizado', 'Finalizado')], max_length=100, null=True, verbose_name='Estado'),
        ),
    ]

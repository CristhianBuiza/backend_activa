# Generated by Django 4.2 on 2024-03-31 17:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('help', '0004_help_state'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='help',
            name='scream',
        ),
        migrations.AddField(
            model_name='help',
            name='screen',
            field=models.CharField(default=django.utils.timezone.now, max_length=100, verbose_name='pantalla'),
            preserve_default=False,
        ),
    ]
# Generated by Django 4.2 on 2024-03-22 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_alter_profile_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='additionalCellphone',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='cellphone',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
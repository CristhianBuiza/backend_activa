# Generated by Django 4.2 on 2024-03-25 03:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('help', '0002_requestattention'),
    ]

    operations = [
        migrations.AddField(
            model_name='help',
            name='details',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
    ]

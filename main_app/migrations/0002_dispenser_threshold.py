# Generated by Django 5.1.3 on 2024-11-16 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dispenser',
            name='threshold',
            field=models.PositiveIntegerField(default=10, help_text='Low level threshold percentage'),
        ),
    ]
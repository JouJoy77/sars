# Generated by Django 4.2.1 on 2023-06-17 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docs', '0006_achievement_is_rejected'),
    ]

    operations = [
        migrations.AlterField(
            model_name='achievement',
            name='title',
            field=models.CharField(max_length=70, verbose_name='Краткое название'),
        ),
        migrations.AlterField(
            model_name='availableachievement',
            name='title',
            field=models.CharField(max_length=70, verbose_name='Краткое название'),
        ),
    ]

# Generated by Django 3.1 on 2021-04-23 18:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20210423_2355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='activation_date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]
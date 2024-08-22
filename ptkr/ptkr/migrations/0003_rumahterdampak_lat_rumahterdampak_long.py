# Generated by Django 4.2.15 on 2024-08-14 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ptkr', '0002_alter_rumahterdampak_dusun_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='rumahterdampak',
            name='lat',
            field=models.FloatField(default=-7.235668071995708, verbose_name='Latitude'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rumahterdampak',
            name='long',
            field=models.FloatField(default=109.041626, verbose_name='Longitude'),
            preserve_default=False,
        ),
    ]
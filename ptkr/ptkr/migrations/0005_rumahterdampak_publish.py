# Generated by Django 4.2.15 on 2024-08-15 02:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ptkr', '0004_rumahterdampak_ket_plantai_rumahterdampak_ket_tangga'),
    ]

    operations = [
        migrations.AddField(
            model_name='rumahterdampak',
            name='publish',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Tanggal diunggah'),
            preserve_default=False,
        ),
    ]
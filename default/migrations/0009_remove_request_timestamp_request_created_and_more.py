# Generated by Django 4.1.7 on 2023-03-08 01:13

import default.models
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('default', '0008_alter_request_options_alter_requeststatus_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='request',
            name='timestamp',
        ),
        migrations.AddField(
            model_name='request',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='request',
            name='additional_requirements',
            field=models.TextField(blank=True, null=True, verbose_name='Дополнительные требования'),
        ),
        migrations.AlterField(
            model_name='request',
            name='color',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Цвет'),
        ),
        migrations.AlterField(
            model_name='request',
            name='last_update',
            field=default.models.AutoDateTimeField(default=django.utils.timezone.now, verbose_name='Дата обновления'),
        ),
        migrations.AlterField(
            model_name='request',
            name='max_age',
            field=models.IntegerField(blank=True, null=True, verbose_name='Год выпуска от'),
        ),
    ]

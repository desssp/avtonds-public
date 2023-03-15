# Generated by Django 4.1.7 on 2023-03-08 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('default', '0012_offerstatus_request_body_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='full_name',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Полное наименование'),
        ),
        migrations.AddField(
            model_name='user',
            name='short_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Краткое наименование'),
        ),
    ]
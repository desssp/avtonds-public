# Generated by Django 4.1.7 on 2023-03-07 23:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('default', '0003_alter_carmodel_year_from_alter_carmodel_year_to'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carmodel',
            name='model_class',
        ),
    ]

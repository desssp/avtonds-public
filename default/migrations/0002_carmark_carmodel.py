# Generated by Django 4.1.7 on 2023-03-07 23:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('default', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarMark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mark_char_id', models.CharField(max_length=150, verbose_name='Текстовый идентификатор')),
                ('name', models.CharField(max_length=150, verbose_name='Наименование')),
                ('name_cyrillic', models.CharField(max_length=150, verbose_name='Наименование на русском')),
                ('rating', models.IntegerField(default=0, verbose_name='Уровень популярности')),
                ('country', models.CharField(max_length=150, verbose_name='Страна производства')),
            ],
            options={
                'verbose_name': 'Марка',
                'verbose_name_plural': 'Марки',
            },
        ),
        migrations.CreateModel(
            name='CarModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_char_id', models.CharField(max_length=150, verbose_name='Текстовый идентификатор')),
                ('name', models.CharField(max_length=150, verbose_name='Наименование')),
                ('name_cyrillic', models.CharField(max_length=150, verbose_name='Наименование на русском')),
                ('model_class', models.CharField(max_length=20, verbose_name='Класс авто')),
                ('year_from', models.DateTimeField(verbose_name='Дата начала производства')),
                ('year_to', models.DateTimeField(null=True, verbose_name='Дата окончания производства')),
                ('car_mark', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='default.carmark')),
            ],
            options={
                'verbose_name': 'Модель',
                'verbose_name_plural': 'Модели',
            },
        ),
    ]

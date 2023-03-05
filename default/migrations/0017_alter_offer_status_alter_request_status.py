# Generated by Django 4.1.7 on 2023-03-13 17:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('default', '0016_delete_testmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='status',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='default.offerstatus', verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='request',
            name='status',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='default.requeststatus', verbose_name='Статус'),
        ),
    ]

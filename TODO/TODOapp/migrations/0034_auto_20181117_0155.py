# Generated by Django 2.1.3 on 2018-11-17 00:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TODOapp', '0033_auto_20181117_0155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='board',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='TODOapp.Board'),
        ),
    ]

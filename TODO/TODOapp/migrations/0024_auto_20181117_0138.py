# Generated by Django 2.1.3 on 2018-11-17 00:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TODOapp', '0023_auto_20181117_0137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='board',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='TODOapp.Board'),
        ),
        migrations.AlterUniqueTogether(
            name='todo',
            unique_together={('board', 'created')},
        ),
    ]

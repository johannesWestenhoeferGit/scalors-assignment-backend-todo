# Generated by Django 2.1.3 on 2018-11-17 22:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TODOapp', '0091_auto_20181117_2327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reminder',
            name='delay',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='todo',
            name='board',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='TODOapp.Board'),
        ),
    ]

# Generated by Django 2.1.3 on 2018-11-17 13:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TODOapp', '0075_auto_20181117_1325'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reminder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('text', models.TextField()),
                ('delay', models.TimeField()),
            ],
        ),
        migrations.AlterField(
            model_name='todo',
            name='board',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='TODOapp.Board'),
        ),
    ]

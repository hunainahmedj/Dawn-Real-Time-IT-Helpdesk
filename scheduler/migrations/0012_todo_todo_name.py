# Generated by Django 2.2.4 on 2019-08-08 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0011_todo'),
    ]

    operations = [
        migrations.AddField(
            model_name='todo',
            name='todo_name',
            field=models.CharField(default='todo', max_length=255),
            preserve_default=False,
        ),
    ]
# Generated by Django 2.2.4 on 2019-08-08 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0012_todo_todo_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notidication', models.CharField(max_length=255)),
            ],
        ),
    ]
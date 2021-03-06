# Generated by Django 2.2.4 on 2019-08-06 18:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0006_ticket_ticket_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='ticket_priority',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='scheduler.Priority'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='ticket_status',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='scheduler.Status'),
        ),
    ]

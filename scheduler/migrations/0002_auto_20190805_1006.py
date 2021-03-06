# Generated by Django 2.2.4 on 2019-08-05 10:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('scheduler', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='staff_assigned',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ticket',
            name='ticket_priority',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scheduler.Priority'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='user_department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scheduler.Department'),
        ),
        migrations.AddField(
            model_name='staffprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='notes',
            name='staff_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='notes',
            name='ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scheduler.Ticket'),
        ),
    ]

# Generated by Django 4.1 on 2022-08-09 09:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_roommember_rtctoken_alter_room_ended_on'),
    ]

    operations = [
        migrations.AddField(
            model_name='roommember',
            name='join_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='roommember',
            name='leave_time',
            field=models.DateTimeField(null=True),
        ),
    ]

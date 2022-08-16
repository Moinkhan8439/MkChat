# Generated by Django 4.1 on 2022-08-08 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_alter_room_host_alter_roommember_room_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='roommember',
            name='RTCToken',
            field=models.CharField(default=0, max_length=250),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='room',
            name='ended_on',
            field=models.DateTimeField(null=True),
        ),
    ]
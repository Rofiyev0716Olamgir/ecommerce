# Generated by Django 4.2.11 on 2024-05-14 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_usertoken'),
    ]

    operations = [
        migrations.AddField(
            model_name='usertoken',
            name='is_used',
            field=models.BooleanField(default=False),
        ),
    ]

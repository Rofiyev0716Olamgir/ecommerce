# Generated by Django 4.2.11 on 2024-05-06 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['order', 'id'], 'verbose_name_plural': 'Category'},
        ),
        migrations.AddField(
            model_name='category',
            name='order',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]

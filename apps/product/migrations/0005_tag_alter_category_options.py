# Generated by Django 4.2.11 on 2024-05-06 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_alter_comment_top_level_comment_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('name_en', models.CharField(max_length=100, null=True)),
                ('name_ru', models.CharField(max_length=100, null=True)),
                ('name_uz', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('order', 'id'), 'verbose_name_plural': 'Category'},
        ),
    ]
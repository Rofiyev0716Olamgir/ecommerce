# Generated by Django 4.2.8 on 2024-05-22 21:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_product_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sold_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='category',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='product.category'),
        ),
    ]

# Generated by Django 5.0.1 on 2024-01-26 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_product_image1_product_image2_product_image3_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='best',
            field=models.BooleanField(default=False, verbose_name='فروش ویژه'),
        ),
        migrations.AddField(
            model_name='product',
            name='best_day',
            field=models.BooleanField(default=False, verbose_name='محصول ویژه امروز'),
        ),
        migrations.AlterField(
            model_name='product',
            name='sell_star',
            field=models.BooleanField(default=False, verbose_name='پر\u200cبازدید\u200cترین'),
        ),
        migrations.AlterField(
            model_name='product',
            name='star',
            field=models.BooleanField(default=False, verbose_name='محصولات منتخب'),
        ),
    ]

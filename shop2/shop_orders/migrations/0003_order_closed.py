# Generated by Django 5.0.1 on 2024-01-31 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_orders', '0002_alter_order_options_alter_orderitem_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='closed',
            field=models.BooleanField(default=False, verbose_name='ارسال شده و تمام شده'),
        ),
    ]
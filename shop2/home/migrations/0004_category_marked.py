# Generated by Django 5.0.1 on 2024-01-26 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_alter_category_options_alter_product_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='marked',
            field=models.BooleanField(default=False, verbose_name='دسته بندی برتر'),
        ),
    ]
# Generated by Django 5.0.1 on 2024-01-26 14:23

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('home', '0006_product_best_product_best_day_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nameUser', models.CharField(max_length=20, verbose_name='نام ارسال کننده')),
                ('textComment', models.TextField(verbose_name='متن')),
                ('dateTime', models.DateTimeField(default=django.utils.timezone.now, verbose_name='زمان')),
                ('isActive', models.BooleanField(default=True, verbose_name='فعال')),
                ('forProduct', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.product', verbose_name='برای محصول')),
                ('userComment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='نام کاربری')),
            ],
            options={
                'verbose_name_plural': 'نظرات',
            },
        ),
        migrations.CreateModel(
            name='ReplyComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nameStore', models.CharField(default='فروشگاه', max_length=200, verbose_name='نام پاسخ دهنده')),
                ('replyText', models.TextField(verbose_name='متن جواب')),
                ('dateTime', models.DateTimeField(default=django.utils.timezone.now)),
                ('isActive', models.BooleanField(default=True)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recomment', to='comment.comment', verbose_name='برای نظر :')),
            ],
            options={
                'verbose_name_plural': 'پاسخ ها',
            },
        ),
    ]

from django.db import models
from django.contrib.auth.models import User
from home.models import Product
from django.utils import timezone
from extensions.utils import jalali_converter

# Create your models here.
class Comment(models.Model):
    forProduct  = models.ForeignKey(Product , on_delete=models.CASCADE , verbose_name='برای محصول')
    userComment = models.ForeignKey(User , on_delete=models.CASCADE , verbose_name='نام کاربری')
    nameUser    = models.CharField(max_length=20 , verbose_name='نام ارسال کننده' )
    textComment = models.TextField(verbose_name='متن')
    dateTime    = models.DateTimeField(default=timezone.now , verbose_name='زمان')
    isActive    = models.BooleanField(default=True , verbose_name='فعال')

    def __str__(self) -> str:
        return f'{self.userComment} - {self.textComment[:10]} ...'
    
    def jdate(self):
        return jalali_converter(self.dateTime) 

    class Meta:
        verbose_name_plural = 'نظرات'

class ReplyComment(models.Model):
    comment   = models.ForeignKey(Comment , on_delete=models.CASCADE , related_name='recomment' , verbose_name='برای نظر :')
    nameStore = models.CharField(max_length=200 , default="فروشگاه" , verbose_name='نام پاسخ دهنده')
    replyText = models.TextField(verbose_name='متن جواب')
    dateTime    = models.DateTimeField(default=timezone.now)
    isActive    = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f'{self.nameStore} - {self.replyText[:10]} ...'
    
    def jdate(self):
        return jalali_converter(self.dateTime) 

    class Meta:
        verbose_name_plural = 'پاسخ ها'
from django.db import models
from django.contrib.auth.models import User
from home.models import Product


# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, null=False, blank=False, on_delete=models.CASCADE, related_name="the_user", verbose_name="کاربر")

    # extra fields 

    phone_number=models.CharField(max_length=11, blank=False, unique=True, verbose_name="شماره موبایل")

    province = models.CharField(max_length=200, null=True, blank=True, verbose_name="استان")
    city = models.CharField(max_length=200, null=True, blank=True, verbose_name="شهر")
    full_address = models.TextField(null=True, blank=True, verbose_name="آدرس")
    postal_code = models.CharField(max_length=200, null=True, blank=True, verbose_name="کد پستی")
    receiver = models.CharField(max_length=200, null=True, blank=True, verbose_name="دریافت کننده")


    def __str__(self) -> str:
        return self.user.username
    
    class Meta:
        verbose_name = "مشتری"
        verbose_name_plural = "مشتریان"


    
class OtpCode(models.Model):
    phone_number = models.CharField(max_length=11, unique=True, verbose_name="شماره موبایل")
    code = models.PositiveSmallIntegerField(verbose_name="کد ارسال شده")
    created = models.DateTimeField(auto_now=True, verbose_name="ایجاد شده")

    def __str__(self) -> str:
        return f'{self.phone_number}-{self.code}-{self.created}'
    
    class Meta:
        verbose_name = "کد تایید"
        verbose_name_plural = "کد تایید"
    

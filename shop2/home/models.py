from django.db import models
from ckeditor.fields import RichTextField
from extensions.utils import jalali_converter
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="نام")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="آدرس")
    image = models.ImageField(upload_to="category/%Y/%m/%d", null=True, blank=True, verbose_name="عکس(اختیاری)")
    left = models.BooleanField(default=False, verbose_name="قرار دادن دسته بندی در  سمت چپ منو")
    marked = models.BooleanField(default=False, verbose_name="دسته بندی برتر")

    class Meta:
        ordering = ('name',)
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی‌ها"

    def __str__(self) -> str:
        return self.name
    

class Product(models.Model):
    storeuser = models.ForeignKey(User , on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name="دسته‌بندی")
    name = models.CharField(max_length=200, verbose_name="نام")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="آدرس")
    image = models.ImageField(upload_to="products/%Y/%m/%d", verbose_name="عکس اول")
    image1 = models.ImageField(upload_to="products/%Y/%m/%d", verbose_name="عکس دوم", null=True, blank=True)
    image2 = models.ImageField(upload_to="products/%Y/%m/%d", verbose_name="عکس سوم", null=True, blank=True)
    image3 = models.ImageField(upload_to="products/%Y/%m/%d", verbose_name="عکس چهارم", null=True, blank=True)
    quantity = models.PositiveBigIntegerField(verbose_name="تعداد موجودی")
    description = RichTextField(verbose_name="توضیحات و اطلاعات")
    product_property = RichTextField(config_name='myConfig', verbose_name="ویژگی‌ها", null=True, blank=True)
    price = models.IntegerField(verbose_name="قیمت با تخفیف")
    offer_price = models.IntegerField(null=True, blank=True, verbose_name="قیمت اصلی")
    available = models.BooleanField(default=True, verbose_name="وضعیت دسترسی")
    created = models.DateTimeField(auto_now_add = True, verbose_name="ایجاد شده")
    updated = models.DateTimeField(auto_now=True, verbose_name="به‌روز شده")
    position = models.IntegerField(verbose_name="موقعیت در نمایش")
    star = models.BooleanField(default=False, verbose_name="محصولات منتخب")
    offer = models.BooleanField(default=False, verbose_name="تخفیف خورده")
    sell_star = models.BooleanField(default=False, verbose_name="پر‌بازدید‌ترین")
    best_day = models.BooleanField(default=False, verbose_name="محصول ویژه امروز")
    best = models.BooleanField(default=False, verbose_name="فروش ویژه")
    more_product = models.ManyToManyField("self" , blank=True , null=True)




    class Meta:
        ordering = ("-position",)
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"

    def __str__(self) -> str:
        return self.name
    
    def decrease_quantity(self, amount):
        if self.quantity >= amount:
            self.quantity -= amount
            self.save()
        else:
            # Handle the case where the requested decrease is greater than the available quantity
            raise ValueError("Insufficient quantity available")
        
    def available_check(self):
        if self.quantity < 1:
            self.available = False
        if self.quantity > 1:
            self.available = True
        return self.available
        
    def increase_quantity(self, amount):
        if amount > 10:
            raise ValueError("over load")
        else:
            self.quantity += amount
            self.save()
        
    
    def jcreated(self):
        return jalali_converter(self.created)
        
    
    def jupdated(self):
        return jalali_converter(self.updated)

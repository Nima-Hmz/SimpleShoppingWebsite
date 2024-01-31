from django.db import models
from accounts.models import Customer
from home.models import Product
from django.contrib.auth.models import User
from extensions.utils import jalali_converter

# Create your models here.


class Order(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders', verbose_name="مشتری")
    paid = models.BooleanField(default=False, verbose_name="پرداخت شده")
    closed = models.BooleanField(default=False, verbose_name="تمام شده")
    created = models.DateTimeField(auto_now_add=True, verbose_name="ایجاد شده")
    updated = models.DateTimeField(auto_now=True, verbose_name="به‌روز شده")

    class Meta:
        ordering = ('-paid', 'closed', '-created')
        verbose_name = "سفارش"
        verbose_name_plural = "سفارش‌ها"

    def __str__(self) -> str:
        return f"{self.user} - {str(self.id)}"
    
    def get_total_price(self):
        return sum(item.get_cost() for item in self.items.all())
    
    def jupdated(self):
        return jalali_converter(self.updated)
    
    def jcreated(self):
        return jalali_converter(self.created)
    
class OrderItem(models.Model): 
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="سفارش")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items', verbose_name="محصول")
    price = models.IntegerField(verbose_name="قیمت")
    quantity = models.IntegerField(default=1, verbose_name="تعداد")

    def __str__(self) -> str:
        return str(self.id)
    
    def get_cost(self):
        return self.price*self.quantity

    class Meta:
        verbose_name = "محصول درون سفارش"
        verbose_name_plural = "محصولات درون سفارش"
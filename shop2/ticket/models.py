from django.db import models
from accounts.models import Customer


class Ticket(models.Model):
    user = models.ForeignKey(Customer , on_delete=models.CASCADE , verbose_name= 'کاربر :')
    title = models.CharField(max_length=200 , blank=False , verbose_name='موضوع')
    text = models.TextField(blank=False , verbose_name='متن درخواست')
    status = models.BooleanField(default=False ,verbose_name= 'بررسی شده')
    


    def __str__(self) -> str:
        return str(self.user.user.username)
    
    class Meta:
        verbose_name_plural = 'درخواست ثبت'
from django.contrib import admin
from .models import Customer, OtpCode

# Register your models here.

@admin.register(OtpCode)
class OtpCodeAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'code', 'created')


admin.register(Customer)
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("user", "phone_number", "full_address")
    search_fields = ("user", "phone_number")

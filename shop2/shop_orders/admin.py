from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.

class OrderItemInLine(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ('product',)

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        return super().get_queryset(request).filter(product__storeuser=request.user)
       
    def save_model(self, request, obj, form, change):
        obj.product.storeuser = request.user
        super().save_model(request, obj, form, change)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'jcreated', 'paid', 'closed')
    list_filter = ('paid',)
    inlines = (OrderItemInLine,)


    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        return super().get_queryset(request).filter(items__product__storeuser=request.user)
       
    def save_model(self, request, obj, form, change):
        obj.items.product.storeuser = request.user
        super().save_model(request, obj, form, change)
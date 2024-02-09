from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from .models import Category, Product

admin.site.register(Category)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "slug", "jcreated", "position", "quantity", "available"]
    search_fields = ["name", "slug"]
    list_filter = ["available"]
    #exclude = ('storeuser',)
    readonly_fields = ('storeuser',)

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        return super().get_queryset(request).filter(storeuser=request.user)
    
    
    def save_model(self, request, obj, form, change):
        obj.storeuser = request.user
        super().save_model(request, obj, form, change)
       
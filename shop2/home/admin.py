from django.contrib import admin
from .models import Category, Product

admin.site.register(Category)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "slug", "jcreated", "position", "quantity", "available"]
    search_fields = ["name", "slug"]
    list_filter = ["available"]
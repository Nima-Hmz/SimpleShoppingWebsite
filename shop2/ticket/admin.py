from typing import Any
from django.contrib import admin
from .models import Ticket

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['user' , 'title' , 'text' , 'status']
    readonly_fields = ['user', 'title' , 'text']
    list_editable = ['status']
    list_filter   = ['status']

    def save_model(self, request, obj, form, change):
        Ticket._meta.verbose_name_plural = 'درخواست ثبت'
        return super().save_model(request, obj, form, change)
    
    

from django.contrib import admin
from .models import *


admin.site.register(ReplyComment )

class ReplyInLine(admin.TabularInline):
    model = ReplyComment
    extra = 1

@admin.register(Comment)
class OrderAdmin(admin.ModelAdmin):
    
    inlines = (ReplyInLine,)
    list_filter = ['recomment']

    
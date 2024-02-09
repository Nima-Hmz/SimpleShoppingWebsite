from django.contrib import admin
from .models import *
from django.db.models.signals import pre_save
from django.dispatch import receiver

@admin.register(ReplyComment )
class ReplyCommentAdmin(admin.ModelAdmin):
    list_display = ['comment' , 'nameStore' , 'replyText' ]   
    readonly_fields = ['nameStore']

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        return super().get_queryset(request).filter(comment__forProduct__storeuser=request.user)
       
    def save_model(self, request, obj, form, change):
        obj.comment.forProduct.storeuser = request.user
        super().save_model(request, obj, form, change)




class ReplyInLine(admin.TabularInline):
    model = ReplyComment
    extra = 0
    readonly_fields = ['nameStore']

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        return super().get_queryset(request).filter(comment__forProduct__storeuser=request.user)
       
    def save_model(self, request, obj, form, change):
        obj.comment.forProduct.storeuser = request.user
        super().save_model(request, obj, form, change)
    

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['textComment' , 'forProduct' , 'nameUser' ]    
    inlines = (ReplyInLine,)
    list_filter = ['recomment']
    readonly_fields = ['forProduct' , 'userComment' , 'nameUser' ,'dateTime']

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        return super().get_queryset(request).filter(forProduct__storeuser=request.user)
       
    def save_model(self, request, obj, form, change):
        obj.forProduct.storeuser = request.user
        super().save_model(request, obj, form, change)


    
@receiver(pre_save, sender=ReplyComment)
def song_pre_save(sender, instance, **kwargs):
    import inspect
    for frame_record in inspect.stack():
        if frame_record[3]=='get_response':
            request = frame_record[0].f_locals['request']
            break
    else:
        request = None
    
    instance.nameStore = request.user
from django.contrib import admin
from .models import *
from django import forms

# Register your models here.
@admin.register(Loves)
class LoveAdmin(admin.ModelAdmin):
     list_display = ['title', 'slug', 'body', 'author', 'publish', 'status', 'tag_list', 'news_image']
     list_filter = ['status', 'created', 'publish', 'author', 'tags']  
     search_fields = ['title', 'body'] 
     prepopulated_fields = {'slug': ('title',)}  
     raw_id_fields = ['author']  
     date_hierarchy = 'publish' 
     ordering = ['status', 'publish']
     def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

     def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())
     

@admin.register(Love_Comments) 
class Love_CommentAdmin(admin.ModelAdmin):    
     list_display = ['name', 'email', 'post', 'created', 'active']    
     list_filter = ['active', 'created', 'updated']    
     search_fields = ['name', 'email', 'body']

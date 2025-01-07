from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ['user', 'verb', 'target', 'created']
    list_filter = ['created']
    search_fields = ['verbs']

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity_type', 'object_id', 'content_object', 'date']
    list_filter = ['date']
    search_fields = ['activity_type']

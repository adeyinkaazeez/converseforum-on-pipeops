from django.contrib import admin
from .models import CustomUser, Profile, SubscribedUsers




# Register your models here.
admin.site.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email']

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user',  'date_of_birth',  'about', 'location', 'photo']


class SubscribedUsersAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'created_date')

admin.site.register(SubscribedUsers, SubscribedUsersAdmin)



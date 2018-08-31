from django.contrib import admin
from .models import UserProfile

class UserProfile_TeacherAdmin(admin.ModelAdmin):

    fields = ['username', 'password']

    list_display = ['username']


# Register your models here.


admin.site.register(UserProfile, UserProfile_TeacherAdmin)


from django.contrib import admin
from .models import Institute, UserProfile, GoogleAuth, EmailConfirmation

#from django.contrib import admin


# Register your models here.


class InstituteAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name']


admin.site.register(Institute, InstituteAdmin)


class UserProfileAdmin(admin.ModelAdmin):

    def username(self, obj):
        return obj.user.username

    def email(self, obj):
        return obj.user.email

    list_display = ['username', 'email', 'institute', 'designation', 'phone_number']
    list_filter = ['institute', 'designation']
    search_fields = ['id', 'institute', 'designation', 'phone_number']


admin.site.register(UserProfile, UserProfileAdmin)


class GoogleAuthAdmin(admin.ModelAdmin):
    def username(self, obj):
        return obj.user.username

    def email(self, obj):
        return obj.user.email

    list_display = ['username', 'email', 'google_id', 'salt']
    search_fields = ['id', 'google_id', 'salt']


admin.site.register(GoogleAuth, GoogleAuthAdmin)


class EmailConfirmationAdmin(admin.ModelAdmin):
    def username(self, obj):
        return obj.user.username

    def email(self, obj):
        return obj.user.email

    list_display = ['username', 'email', 'email_confirmed']
    list_filter = ['email_confirmed']
    search_fields = ['id']

admin.site.register(EmailConfirmation, EmailConfirmationAdmin)
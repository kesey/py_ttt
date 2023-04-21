from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from authentication.models import User
from adminplus.sites import AdminSitePlus

admin.site = AdminSitePlus()
admin.autodiscover()

# class UserAdmin(BaseUserAdmin):
#     pass

admin.site.register(User)
# admin.site.register(User, UserAdmin)

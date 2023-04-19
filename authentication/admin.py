from django.contrib import admin
from authentication.models import User
from adminplus.sites import AdminSitePlus

admin.site = AdminSitePlus()
admin.autodiscover()

admin.site.register(User)

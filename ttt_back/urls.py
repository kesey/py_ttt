from django.urls import include, path
from django.contrib import admin
from adminplus.sites import AdminSitePlus
import ttt_back.views

admin.site = AdminSitePlus()
admin.autodiscover()

urlpatterns = [
    path('tinymce/', include('tinymce.urls')),
    path('admin/gestion_exemplaire/<int:id_cassette>/', ttt_back.views.Gestion_exemplaire_detail.as_view(), name="gestion_exemplaire_detail"),
    path('admin/gestion_exemplaire/', ttt_back.views.gestion_exemplaire, name="gestion_exemplaire"),
    path('admin/', admin.site.urls),
]
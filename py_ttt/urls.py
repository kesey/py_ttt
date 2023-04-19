"""
URL configuration for py_ttt project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from adminplus.sites import AdminSitePlus
from django.conf import settings
from django.conf.urls.static import static
import ttt_front.views
import ttt_back.views

admin.site = AdminSitePlus()
admin.autodiscover()

urlpatterns = [
    path('tinymce/', include('tinymce.urls')), 
    path('admin/gestion_exemplaire/<int:id_cassette>/', ttt_back.views.Gestion_exemplaire_detail.as_view(), name="gestion_exemplaire_detail"),
    path('admin/gestion_exemplaire/', ttt_back.views.gestion_exemplaire, name="gestion_exemplaire"),
    path('admin/', admin.site.urls),
    path('', ttt_front.views.home, name='home')
]

if settings.DEBUG: # serve media in dev environnement (don't use this in production)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
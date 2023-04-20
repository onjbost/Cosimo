from django.contrib import admin
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', deactive_cosimo, name='deactive'),
    path('active/', active_cosimo, name="active"),
    
] +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
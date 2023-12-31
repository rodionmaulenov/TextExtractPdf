"""
URL configuration for home_api project.

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
from decouple import config

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from input_text.views import InputTextView
from upload_file.views import FileUploadView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload/', FileUploadView.as_view(), name='upload_file'),
    path('input/', InputTextView.as_view(), name='input_text')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if config('DJANGO_SETTINGS_MODULE') == 'home_api.settings.base':
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

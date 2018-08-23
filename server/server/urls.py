"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path

from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static

from django.shortcuts import render

from django import forms
from simditor.fields import RichTextFormField
from simditor.views import UPLOAD


class SimditorForm(forms.Form):
    content = RichTextFormField()


def IndexView(request):

    context = {'form': SimditorForm()}
    return render(request, 'index.html', context)


urlpatterns = [
    path('admin', admin.site.urls),
    path('', IndexView),
    path('simditor/upload/', UPLOAD)   # add this line
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

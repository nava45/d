"""django_proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from registration.views import register, logout_page, register_success, home, \
    login_page, edit

urlpatterns = [
    url(r'^acc/', include('allauth.urls')),
    url(r'^rest/', include('rest.urls')),
    url(r'^$', login_page),
    url(r'^home/$', home),
    url(r'^edit/$', edit),
    url(r'^logout/$', logout_page),  
    url(r'^admin/', admin.site.urls),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^register/$', register),
    url(r'^register/success/$', register_success),
]

"""FusionCatcherDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url
from rap import views

urlpatterns = [
    url(r'^statistics_all/', views.statistics_all, name='statistics_all'),
    url(r'^get_list/(\w+)/(\w+)/(\w+)/(\d*)/?(\w*)/?$', views.get_list, name='get_list'),
    url(r'^download/', views.download_data, name='download_data'),
    url(r'^explore/(.+)/(\d+)/(\d+)/', views.see_file, name='explore'),
]

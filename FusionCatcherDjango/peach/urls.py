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
from peach import views

urlpatterns = [
    url(r'get_info_all/(\w+)/?(\d*)/$', views.get_info_all, name='get_info_all'),
    url(r'^get_distribution/(\w+)/(\w+)/(\d*)/?(\w*)/?(\w*)/?$', views.get_distribution, name='get_distribution'),
    url(r'^chromosomes/', views.get_chromosomes, name='get_chromosomes'),
    url(r'^genes/', views.get_genes, name='get_genes'),
    url(r'^gene_types/', views.get_gene_types, name='get_gene_types'),
    url(r'^cultivars/', views.get_cultivars, name='get_cultivars'),
    url(r'generate_statistics/*$', views.generate_statistics, name='generate_statistics'),
    url(r'search_by_chromosome/(\w+)/(\d+)/(\d+)/?(\w+)/?(\w+)/$', views.search_by_chromosome, name='search_by_chromosome'),
    url(r'search_by_gene/(\w+)/(.+)/$', views.search_by_gene, name='search_by_gene'),
]

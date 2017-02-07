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
from app import views

urlpatterns = [
    url(r'^events/(.*)/', views.fusion_events, name='fusionEvents'),
    url(r'^genes/([\d]+)/', views.genes, name='genes'),
    url(r'^count_genes/(.+)/', views.count_genes, name='count_genes'),
    url(r'^statistics_all/', views.statistics_all, name='statistics_all'),
    url(r'^statistics/(.+)/', views.statistics, name='statistics'),
    url(r'^print_file/', views.print_file, name='print_file'),
    url(r'^chromosomes/', views.chromosomes, name='chromosomes'),
    url(r'^cell_lines/', views.cell_lines, name='cell_lines'),
    url(r'^get_chromosomes_cell_lines/(.+)', views.get_chromosomes_cell_lines, name='get_chromosomes_cell_lines'),
    url(r'^search_indels_by_region/(.+)/(.+)/(.+)', views.search_indels_by_region, name='search_indels_by_region'),
    url(r'^show_info/(.+)', views.show_info, name='show_info'),
]

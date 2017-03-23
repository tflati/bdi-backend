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
from django.conf.urls import url, include
from django.contrib import admin
from app import views
# url(r'^app/', include('app.urls')),

urlpatterns = [
    url(r'^peach/', include('peach.urls')),
    url(r'^cows/', include('cows.urls')),
    url(r'^rap/', include('rap.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^chromosomes/(.+)/(.+)/(.+)/(.+)/', views.search_for_chromosome, name='search_for_chromosome'),
    url(r'^cell_line/(.+)/', views.search_for_cell_line, name='search_for_cell_line'),
    url(r'^genes/(.+)/(.+)/(.+)/', views.search_for_pair_gene, name='search_for_pair_gene'),
    url(r'^genes/(.+)/(.+)/', views.search_for_single_gene, name='search_for_single_gene'),
    url(r'^genes/(.+)/', views.search_for_single_gene, name='search_for_single_gene'),
    url(r'^exon/single/(.+)/(.+)/', views.search_for_single_exon, name='search_for_single_exon'),
    url(r'^exon/pair/(.+)/(.+)/(.+)/', views.search_for_pair_exon, name='search_for_pair_exon'),
    url(r'^transcript/single/(.+)/(.+)/', views.search_for_single_transcript, name='search_for_single_transcript'),
    url(r'^transcript/pair/(.+)/(.+)/(.+)/', views.search_for_pair_transcript, name='search_for_pair_transcript'),
    url(r'^fusion_information/(.+)/(.+)/(.+)/(.+)/(.+)/', views.search_for_fusion_information, name='search_for_fusion_information'),
    url(r'^chromosomes/', views.chromosomes, name='chromosomes'),
    url(r'^cell_lines/', views.cell_lines, name='cell_lines'),
    url(r'^statistics_all/', views.statistics_all, name='statistics_all'),
    url(r'^statistics_by_chromosome/(.+)/', views.statistics_by_chromosome, name='statistics_by_chromosome'),
    url(r'^fusion_by_chromosome/', views.fusion_by_chromosome, name='statistics_all'),
    url(r'^download_data/', views.download_data, name='download_data'),
    url(r'^genstats/', views.generate_statistics, name='generate_statistics'),
    url(r'^get_distribution/(\w+)/(\w+)/(\d*)/?(\w*)/?$', views.get_distribution, name='get_distribution'),
    url(r'^get_single_distribution/(.+)/(.+)/', views.get_single_distribution, name='get_single_distribution'),
    url(r'^search_for_disease/(.+)/', views.search_for_disease, name='search_for_disease'),
]

"""EDC_Project2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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

from webapp import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.index, name='index'),
    path('movies/', views.movies, name='movies'),
    path('series/', views.series, name='series'),
    path('search_results/<_str>/', views.get_search_results, name='search_results'),
    path('info/<id>/<is_movie>', views.detail_info, name='detail_info'),
    path('my_list/', views.playlist, name='playlist'),
    path('film_years/', views.film_by_year, name='film_years'),
    path('film_years/<mov_name>/', views.film_from_dbpedia, name='film_years_info'),
]

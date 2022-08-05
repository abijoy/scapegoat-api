from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('news/top-news', views.get_top_news, name='get_top_news'),
    path('news/geo-top-news', views.get_geo_top_news, name='get_geo_top_news'),
    path('music/recommendation', views.get_music_recom_track, name='get_music_recom_track')
]
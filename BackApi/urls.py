from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search_movie),
    path('api/movie-details/', views.movie_details, name='movie_details'),
]

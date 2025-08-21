# Agrega este nuevo endpoint a tu views.py de Django
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from rest_framework import status

# Tu endpoint actual se mantiene igual
@api_view(['GET'])
def search_movie(request):
    query = request.query_params.get('q','')
    if not query:         
        return Response({"error": "Por favor, campo requerido"})
        
    API_KEY='d13b2f22'
    url = f'http://www.omdbapi.com/?apikey={API_KEY}&s={query}'
    
    try:
        external_response = requests.get(url)
        external_response.raise_for_status()
        data = external_response.json()
    except requests.exceptions.RequestException as e:
        return Response({"error": str(e)}, status=status.HTTP_502_BAD_GATEWAY)
        
    if "Search" in data:
        necesary_data=[
            {"title": movie.get("Title"), "imdb_Id": movie.get("imdbID")}
            for movie in data["Search"]
        ]
        print(necesary_data)
    else:         
        necesary_data = {"error:":data.get("Error","No se encontraron resultados")}
     
    return Response(necesary_data)

# NUEVO ENDPOINT para obtener detalles con portadas
# Agrega esta nueva view a tu archivo views.py en Django

@api_view(['GET'])
def movie_details(request):
    title = request.query_params.get('title', '')
    
    if not title:
        return Response({"error": "Título requerido"}, status=status.HTTP_400_BAD_REQUEST)
    
    # API Key de TMDB (reemplaza con tu key real)
    TMDB_API_KEY = 'TU_API_KEY_DE_TMDB_AQUI'
    
    # Buscar película en TMDB por título
    search_url = f'https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={title}&language=es-ES'
    
    try:
        response = requests.get(search_url)
        response.raise_for_status()
        data = response.json()
        
        if data['results']:
            movie = data['results'][0]  # Tomar el primer resultado
            
            movie_details = {
                'title': movie.get('title', title),
                'year': movie.get('release_date', '')[:4] if movie.get('release_date') else '',
                'poster': f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie.get('poster_path') else None,
                'backdrop': f"https://image.tmdb.org/t/p/w1280{movie['backdrop_path']}" if movie.get('backdrop_path') else None,
                'description': movie.get('overview', ''),
                'rating': round(movie.get('vote_average', 0), 1),
                'genre': ', '.join([genre['name'] for genre in movie.get('genres', [])]) if movie.get('genres') else ''
            }
            
            return Response(movie_details)
        else:
            return Response({"error": "Película no encontrada"}, status=status.HTTP_404_NOT_FOUND)
            
    except requests.exceptions.RequestException as e:
        return Response({"error": str(e)}, status=status.HTTP_502_BAD_GATEWAY)

# También necesitas agregar esta URL a tu urls.py:
# path('api/movie-details/', views.movie_details, name='movie_details'),

# También agrega este endpoint para películas populares
@api_view(['GET'])
def get_popular_movies(request):
    TMDB_API_KEY = 'TU_API_KEY_DE_TMDB_AQUI'
    url = f'https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}&language=es-ES&page=1'
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        movies = []
        for movie in data.get('results', [])[:10]:  # Limitamos a 10 películas
            movies.append({
                "title": movie.get('title'),
                "imdb_Id": f"tt{movie.get('id')}",  # TMDB ID convertido
                "poster": f"https://image.tmdb.org/t/p/w500{movie.get('poster_path')}" if movie.get('poster_path') else None,
                "description": movie.get('overview', 'Sin descripción disponible'),
                "year": movie.get('release_date', '')[:4] if movie.get('release_date') else 'N/A',
                "rating": movie.get('vote_average', 0),
                "backdrop": f"https://image.tmdb.org/t/p/w1280{movie.get('backdrop_path')}" if movie.get('backdrop_path') else None
            })
        
        return Response(movies)
    except:
        # Respaldo con películas hardcodeadas si TMDB falla
        return Response([
            {"title": "Película Popular 1", "imdb_Id": "tt0000001", "poster": None, "description": "Descripción no disponible", "year": "2024", "rating": "8.0", "backdrop": None},
            {"title": "Película Popular 2", "imdb_Id": "tt0000002", "poster": None, "description": "Descripción no disponible", "year": "2024", "rating": "7.5", "backdrop": None}
        ])

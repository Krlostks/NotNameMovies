from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from rest_framework import status

@api_view (['GET'])
def search_movie(request):
    query = request.query_params.get('q','')

    if not query: 
        return Response({"error": "Por favor, campo requerido"})
    
    API_KEY='d13b2f22'
    url = f'http://www.omdbapi.com/?apikey={API_KEY}&s={query}'

    #este try consume elapi y almacena todo en data
    try:
        external_response = requests.get(url)
        external_response.raise_for_status()
        data = external_response.json()
    except requests.exceptions.RequestException as e:
        return Response({"error": str(e)}, status=status.HTTP_502_BAD_GATEWAY)
    
    #aqui proceso el data para mandar al front los datos necesarios
    if "Search" in data:
        necesary_data=[
            {"title": movie.get("Title"), "imdb_Id": movie.get("imdbID")}
            for movie in data["Search"]
        ]
        print(necesary_data)
    else: 
        necesary_data = {"error:":data.get("Error","No se encontraron resultados")} 
    return Response(necesary_data)


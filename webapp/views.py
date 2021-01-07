import json

from django.shortcuts import render
from s4api.graphdb_api import GraphDBApi
from s4api.swagger import ApiClient

endpoint = "http://localhost:7200"
repo_name = "movies_db"
client = ApiClient(endpoint=endpoint)
accessor = GraphDBApi(client)


# Create your views here.
def index(request):
    # select top 10 movies
    query = """"
    PREFIX mov:<http://digital-media.com/pred/>
    SELECT ?poster, ?name, ?rating
    WHERE {
    }
    """
    payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query,
                                 repo_name=repo_name)
    res = json.loads(res)
    top_movies = []
    for e in res['results']['bindings']:
        for v in e.values():
            top_movies.append(v['value'])

    query = """"
        PREFIX ser:<http://digital-media.com/pred/>
        SELECT ?poster, ?name, ?rating
        WHERE {
        }
        """
    payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query,
                                 repo_name=repo_name)
    res = json.loads(res)
    top_series = []
    for e in res['results']['bindings']:
        for v in e.values():
            top_series.append(v['value'])

    #tparams = {
      #  'movies' : top_movies,
      #  'series' : top_series,
    #}

    return render(request, 'index.html')

def movies(request):

    return render(request, 'movies_list.html')

def series(request):

    return render(request, 'series_list.html')

def get_search_results(request):

    return render(request, 'search_result.html')

def detail_info(request):

    return render(request, 'info.html')

def full_news(request):

    return render(request, 'news.html')
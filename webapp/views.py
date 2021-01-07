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
    """payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query,
                                 repo_name=repo_name)
    res = json.loads(res)
    top_movies = []
    for e in res['results']['bindings']:
        for v in e.values():
            top_movies.append(v['value'])"""

    query = """"
        PREFIX ser:<http://digital-media.com/pred/>
        SELECT ?poster, ?name, ?rating
        WHERE {
        }
        """
    """payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query,
                                 repo_name=repo_name)
    res = json.loads(res)
    top_series = []
    for e in res['results']['bindings']:
        for v in e.values():
            top_series.append(v['value'])"""

    #tparams = {
      #  'movies' : top_movies,
      #  'series' : top_series,
    #}

    return render(request, 'index.html')

def movies(request):

    movies = [];
    movies.append(1);
    movies.append(2);
    movies.append(3);
    movies.append(4);
    movies.append(5);
    movies.append(6);
    movies.append(7);
    movies.append(8);
    movies.append(9);
    movies.append(10);
    movies.append(4);
    movies.append(5);
    movies.append(6);
    movies.append(7);
    movies.append(8);
    movies.append(9);
    movies.append(10);



    tparams = {
        'movies': movies,
    }

    return render(request, 'movies_list.html', tparams)

def series(request):
    series = [];
    series.append(1);
    series.append(2);
    series.append(3);
    series.append(4);
    series.append(5);
    series.append(6);
    series.append(7);
    series.append(8);
    series.append(9);
    series.append(10);
    series.append(4);
    series.append(5);
    series.append(6);
    series.append(7);
    series.append(8);
    series.append(9);
    series.append(10);

    tparams = {
        'series': series,
    }

    return render(request, 'series_list.html', tparams)

def get_search_results(request):

    return render(request, 'search_result.html')

def detail_info(request):

    return render(request, 'info.html')

def full_news(request):

    return render(request, 'news.html')
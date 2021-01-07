import json

from django.shortcuts import render
from s4api.graphdb_api import GraphDBApi
from s4api.swagger import ApiClient

IMAGES_SITE = "http://image.tmdb.org/t/p/w200"
endpoint = "http://localhost:7200"
repo_name = "movies_db"
client = ApiClient(endpoint=endpoint)
accessor = GraphDBApi(client)


# Create your views here.
def index(request):
    # select top 10 movies
    query = """
            PREFIX mov:<http://moviesProject.org/sub/mov/>
            PREFIX pred:<http://moviesProject.org/pred/>
            SELECT ?movie ?id ?poster ?title ?has_score
            WHERE {
            ?movie pred:poster ?id .
            ?movie pred:poster ?poster .
            ?movie pred:title ?title .
            ?movie pred:has_score ?has_score .
            }
            ORDER BY DESC(?has_score) LIMIT 10
            """
    payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query,
                                 repo_name=repo_name)
    print(res)

    res = json.loads(res)
    top_movies = []
    for e in res['results']['bindings']:
        movie_tmp = []
        movie_tmp.append(e['id']['value'])
        movie_tmp.append(e['title']['value'])
        poster = IMAGES_SITE + str(e['poster']['value'])
        movie_tmp.append(poster)
        movie_tmp.append(e['has_score']['value'])
        top_movies.append(movie_tmp)


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

    tparams = {
      'top_movies': top_movies,
      #  'series' : top_series,
    }

    return render(request, 'index.html', tparams)

def movies(request):
    #select all movies
    query = """
        PREFIX mov:<http://moviesProject.org/sub/mov/>
        PREFIX pred:<http://moviesProject.org/pred/>
        SELECT ?movie ?id ?poster ?title
        WHERE {
            ?movie pred:id ?id .
            ?movie pred:poster ?poster .
            ?movie pred:title ?title .
        }"""
    payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query,
                                 repo_name=repo_name)

    res = json.loads(res)
    movies_all = []
    for e in res['results']['bindings']:
        movie_tmp = []
        movie_tmp.append(e['id']['value'])
        movie_tmp.append(e['title']['value'])
        poster = IMAGES_SITE + str(e['poster']['value'])
        movie_tmp.append(poster)
        movies_all.append(movie_tmp)

    print(movies_all)



    tparams = {
        'movies_all': movies_all,
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
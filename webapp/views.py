import json
from webapp import queries
from django.http import HttpResponseRedirect
from django.shortcuts import render
from s4api.graphdb_api import GraphDBApi
from s4api.swagger import ApiClient

IMAGES_SITE = "http://image.tmdb.org/t/p/w200"
NO_IMAGE = "../static/assets/img/NoImage.jpg"
endpoint = "http://localhost:7200"
repo_name = "movies_db"
client = ApiClient(endpoint=endpoint)
accessor = GraphDBApi(client)

# Create your views here.

def get_top_movies():
    # select top 10 movies
    query = """
                PREFIX pred:<http://moviesProject.org/pred/>
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                SELECT ?id ?poster ?title ?has_score
                WHERE {
                    ?movie pred:id_m ?id .
                    ?movie pred:poster ?poster .
                    ?movie pred:title ?title .
                    ?movie pred:has_score ?has_score .
                }
                ORDER BY DESC(xsd:float(?has_score)) LIMIT 10
                """
    payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query,
                                 repo_name=repo_name)

    res = json.loads(res)
    top_movies = []
    for e in res['results']['bindings']:
        movie_tmp = []
        movie_tmp.append(e['id']['value'])
        movie_tmp.append(e['title']['value'])
        if str(e['poster']['value']) is not "":
            poster = IMAGES_SITE + str(e['poster']['value'])
        else:
            poster = NO_IMAGE
        movie_tmp.append(poster)
        movie_tmp.append(e['has_score']['value'])
        top_movies.append(movie_tmp)

    return top_movies

def get_top_series():
    query = """
                PREFIX pred:<http://moviesProject.org/pred/>
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                SELECT ?id ?poster ?title ?has_score
                WHERE {
                    ?serie pred:id_s ?id .
                    ?serie pred:poster ?poster .
                    ?serie pred:title ?title .
                    ?serie pred:has_score ?has_score .
                }
                ORDER BY DESC(xsd:float(?has_score)) LIMIT 10
                """

    payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query,
                                 repo_name=repo_name)

    print(res)

    res = json.loads(res)
    top_series = []
    for e in res['results']['bindings']:
        serie_tmp = []
        serie_tmp.append(e['id']['value'])
        serie_tmp.append(e['title']['value'])
        if str(e['poster']['value']) is not "":
            poster = IMAGES_SITE + str(e['poster']['value'])
        else:
            poster = NO_IMAGE
        serie_tmp.append(poster)
        serie_tmp.append(e['has_score']['value'])
        top_series.append(serie_tmp)

    return top_series

def index(request):

    top_movies = get_top_movies()
    top_series = get_top_series()

    if 'info-m' in request.POST:
        id = request.POST.get('info-m')
        detail_info(request, id)
        return HttpResponseRedirect('/info/' + id)

    tparams = {
      'top_movies': top_movies,
      'top_series': top_series,
    }

    return render(request, 'index.html', tparams)

def get_genres():
    #movies and series genres
    query = """
        PREFIX pred:<http://moviesProject.org/pred/>
        SELECT DISTINCT ?genre_m
        WHERE {
            ?movie pred:genre ?genre_m .
        }
        ORDER BY ASC(?genre_m)
        """

    payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query,
                                 repo_name=repo_name)

    res = json.loads(res)
    genres = []
    for e in res['results']['bindings']:
        for v in e.values():
            genres.append(v['value'])

    return genres

def movies(request, filter = None, order = None):
    query_movies_score = """
                    PREFIX mov:<http://moviesProject.org/sub/mov/>
                    PREFIX pred:<http://moviesProject.org/pred/>
                    SELECT ?movie ?id ?poster ?title ?has_score
                    WHERE {
                        ?movie pred:id_m ?id .
                        ?movie pred:poster ?poster .
                        ?movie pred:title ?title .
                        ?movie pred:has_score ?has_score .
                    }
                    ORDER BY DESC(xsd:float(?has_score))

                    """ 
    query_movies_score_genre = """
                    PREFIX mov:<http://moviesProject.org/sub/mov/>
                    PREFIX pred:<http://moviesProject.org/pred/>
                    SELECT ?movie ?id ?poster ?title ?has_score
                    WHERE 
                    {{
                    {{
                        ?movie pred:id_m ?id .
                        ?movie pred:poster ?poster .
                        ?movie pred:title ?title .
                        ?movie pred:has_score ?has_score .
                    }}
                        {}
                    }}
                    ORDER BY DESC(xsd:float(?has_score))

                    """ 

    query_movies_alphabetic_genre = """
                            PREFIX mov:<http://moviesProject.org/sub/mov/>
                            PREFIX pred:<http://moviesProject.org/pred/>
                            SELECT ?movie ?id ?poster ?title ?has_score
                            WHERE 
                            {{
                            {{
                            ?movie pred:id_m ?id .
                            ?movie pred:poster ?poster .
                            ?movie pred:title ?title .
                            ?movie pred:has_score ?has_score .
                            }}
                            {}
                            }}
                            ORDER BY DESC(?title)
                          """
    query_movies_alphabetic = """
                            PREFIX mov:<http://moviesProject.org/sub/mov/>
                            PREFIX pred:<http://moviesProject.org/pred/>
                            SELECT ?movie ?id ?poster ?title ?has_score
                            WHERE {
                            ?movie pred:id_m ?id .
                            ?movie pred:poster ?poster .
                            ?movie pred:title ?title .
                            ?movie pred:has_score ?has_score .
                            }
                            ORDER BY DESC(?title)
                          """

    query_movies_popularity = """
                        PREFIX mov:<http://moviesProject.org/sub/mov/>
                        PREFIX pred:<http://moviesProject.org/pred/>
                        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                        SELECT ?movie ?id ?poster ?title ?has_score ?popularity
                        WHERE {
                            ?movie pred:id_m ?id .
                            ?movie pred:poster ?poster .
                            ?movie pred:title ?title .
                            ?movie pred:has_score ?has_score .
                            ?movie pred:popularity ?popularity .
                        }
                        ORDER BY DESC(xsd:float(?popularity))
                        """

    query_movies_popularity_genre = """
                        PREFIX mov:<http://moviesProject.org/sub/mov/>
                        PREFIX pred:<http://moviesProject.org/pred/>
                        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                        SELECT ?movie ?id ?poster ?title ?has_score ?popularity
                        WHERE 
                        {{
                        {{
                            ?movie pred:id_m ?id .
                            ?movie pred:poster ?poster .
                            ?movie pred:title ?title .
                            ?movie pred:has_score ?has_score .
                            ?movie pred:popularity ?popularity .
                        }}
                        {}
                        }}
                        ORDER BY DESC(xsd:float(?popularity))
                        """

    if filter is None and request.POST.get('checkbox'):
        myDict = dict(request.POST.lists())
        _filter = myDict['checkbox']
        if 'order' in myDict:
            _order = myDict['order'][0]
        else:
            _order = None
        return movies(request, _filter, _order)

    elif request.POST.get('checkbox'):
        query_genre = """
                    PREFIX pred:<http://moviesProject.org/pred/> 
                        SELECT ?movie ?id ?poster ?title ?has_score
                        WHERE {{
                            ?movie pred:id_m ?id .
                            ?movie pred:poster ?poster .
                            ?movie pred:title ?title .
                            ?movie pred:has_score ?has_score .
                            {}
                        }}
                        """
        intersect_query_genre =  """
                                {{
                                        ?movie pred:id_m ?id .
                                        ?movie pred:poster ?poster .
                                        ?movie pred:title ?title .
                                        ?movie pred:has_score ?has_score .
                                        {}
                                }}
                                """
        if request.POST.get('order'):
            add_to_query = ""
            for filt in filter:
                add_to_query += '?movie pred:genre "{}" .\n'.format(str(filt))
            if order == "Average":    
                query = query_movies_score_genre.format(add_to_query)
            elif order == "Popularity":
                query = query_movies_popularity_genre.format(add_to_query)
            else:
                query = query_movies_alphabetic_genre.format(add_to_query)
        else:
            add_to_query = ""
            for filt in filter:
                add_to_query += '?movie pred:genre "{}" .\n'.format(str(filt)) 
            query = query_genre.format(add_to_query)
    else:
        if request.POST.get('order'):
            myDict = dict(request.POST.lists())
            order = myDict['order'][0]
            if order == "Average":
                query = query_movies_score
            elif order == "Popularity":
                query = query_movies_popularity
            else:
                query = query_movies_alphabetic
        else:
            query = """
                    PREFIX mov:<http://moviesProject.org/sub/mov/>
                    PREFIX pred:<http://moviesProject.org/pred/>
                    SELECT ?movie ?id ?poster ?title
                    WHERE {
                        ?movie pred:id_m ?id .
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
        if str(e['poster']['value']) is not "":
            poster = IMAGES_SITE + str(e['poster']['value'])
        else:
            poster = NO_IMAGE
        movie_tmp.append(poster)
        movies_all.append(movie_tmp)

    mgenres = get_genres()

    if 'info-m' in request.POST:
        id = request.POST.get('info-m')
        detail_info(request, id)
        return HttpResponseRedirect('/info/' + id)

    tparams = {
        'movies_all': movies_all,
        'movie_genres': mgenres,
    }

    return render(request, 'movies_list.html', tparams)

def series(request):
    # select all series
    query = """
            PREFIX pred:<http://moviesProject.org/pred/>
            SELECT ?id ?poster ?title
            WHERE {
                ?serie pred:id_s ?id .
                ?serie pred:poster ?poster .
                ?serie pred:title ?title .
            }"""
    payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query,
                                 repo_name=repo_name)


    print(res)

    res = json.loads(res)
    series_all = []
    for e in res['results']['bindings']:
        serie_tmp = []
        serie_tmp.append(e['id']['value'])
        serie_tmp.append(e['title']['value'])
        if str(e['poster']['value']) is not "":
            poster = IMAGES_SITE + str(e['poster']['value'])
        else:
            poster = NO_IMAGE
        serie_tmp.append(poster)
        series_all.append(serie_tmp)

    print(series_all)

    sgenres = get_genres()

    if 'info-m' in request.POST:
        id = request.POST.get('info-m')
        detail_info(request, id)
        return HttpResponseRedirect('/info/' + id)

    tparams = {
        'series_all': series_all,
        'series_genres': sgenres,
    }

    return render(request, 'series_list.html', tparams)

def get_search_results(request):

    return render(request, 'search_result.html')

def detail_info(request, id):

    return render(request, 'info.html')

def playlist(request):
    fav = get_top_movies()

    tparams = {
        'fav': fav,
    }

    return render(request, 'playlist.html', tparams)

def full_news(request):

    return render(request, 'news.html')

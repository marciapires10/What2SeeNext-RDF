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
    if 'search' in request.POST:
        _str = request.POST.get('search', '')
        return HttpResponseRedirect('/search_results/' + _str)

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

def get_movies_genres():
    #movies genres
    query = """
        PREFIX pred:<http://moviesProject.org/pred/>
        SELECT DISTINCT ?genre_m
        WHERE {
            ?movie pred:id_m ?id .
            ?movie pred:genre ?genre_m .
        }
        ORDER BY ASC(?genre_m)
        """

    payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query,
                                 repo_name=repo_name)

    res = json.loads(res)
    m_genres = []
    for e in res['results']['bindings']:
        for v in e.values():
            m_genres.append(v['value'])

    return m_genres
    
def get_series_genres():
    #series genres
    query = """
        PREFIX pred:<http://moviesProject.org/pred/>
        SELECT DISTINCT ?genre_s
        WHERE {
            ?serie pred:id_s ?id .
            ?serie pred:genre ?genre_s .
        }
        ORDER BY ASC(?genre_s)
        """

    payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query,
                                 repo_name=repo_name)

    res = json.loads(res)
    s_genres = []
    for e in res['results']['bindings']:
        for v in e.values():
            s_genres.append(v['value'])

    return s_genres

def movies(request, filter = None, order = None):
    if 'search' in request.POST:
        _str = request.POST.get('search', '')
        return HttpResponseRedirect('/search_results/' + _str)

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

    mgenres = get_movies_genres()

    if 'info-m' in request.POST:
        id = request.POST.get('info-m')
        detail_info(request, id)
        return HttpResponseRedirect('/info/' + id)

    tparams = {
        'movies_all': movies_all,
        'movie_genres': mgenres,
    }

    return render(request, 'movies_list.html', tparams)

def series(request, filter = None, order = None):
    if 'search' in request.POST:
        _str = request.POST.get('search', '')
        return HttpResponseRedirect('/search_results/' + _str)

    query_series_score = """
                    PREFIX serie:<http://moviesProject.org/sub/serie/>
                    PREFIX pred:<http://moviesProject.org/pred/>
                    SELECT ?movie ?id ?poster ?title ?has_score
                    WHERE {
                        ?movie pred:id_s ?id .
                        ?movie pred:poster ?poster .
                        ?movie pred:title ?title .
                        ?movie pred:has_score ?has_score .
                    }
                    ORDER BY DESC(xsd:float(?has_score))

                    """ 
    query_series_score_genre = """
                    PREFIX serie:<http://moviesProject.org/sub/serie/>
                    PREFIX pred:<http://moviesProject.org/pred/>
                    SELECT ?serie ?id ?poster ?title ?has_score
                    WHERE 
                    {{
                    {{
                        ?serie pred:id_s ?id .
                        ?serie pred:poster ?poster .
                        ?serie pred:title ?title .
                        ?serie pred:has_score ?has_score .
                    }}
                        {}
                    }}
                    ORDER BY DESC(xsd:float(?has_score))

                    """ 

    query_series_alphabetic_genre = """
                            PREFIX serie:<http://moviesProject.org/sub/serie/>
                            PREFIX pred:<http://moviesProject.org/pred/>
                            SELECT ?serie ?id ?poster ?title ?has_score
                            WHERE 
                            {{
                            {{
                            ?serie pred:id_s ?id .
                            ?serie pred:poster ?poster .
                            ?serie pred:title ?title .
                            ?serie pred:has_score ?has_score .
                            }}
                            {}
                            }}
                            ORDER BY DESC(?title)
                          """
    query_series_alphabetic = """
                            PREFIX serie:<http://moviesProject.org/sub/serie/>
                            PREFIX pred:<http://moviesProject.org/pred/>
                            SELECT ?serie ?id ?poster ?title ?has_score
                            WHERE {
                            ?serie pred:id_s ?id .
                            ?serie pred:poster ?poster .
                            ?serie pred:title ?title .
                            ?serie pred:has_score ?has_score .
                            }
                            ORDER BY DESC(?title)
                          """

    query_series_popularity = """
                        PREFIX serie:<http://moviesProject.org/sub/serie/>
                        PREFIX pred:<http://moviesProject.org/pred/>
                        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                        SELECT ?serie ?id ?poster ?title ?has_score ?popularity
                        WHERE {
                            ?serie pred:id_s ?id .
                            ?serie pred:poster ?poster .
                            ?serie pred:title ?title .
                            ?serie pred:has_score ?has_score .
                            ?serie pred:popularity ?popularity .
                        }
                        ORDER BY DESC(xsd:float(?popularity))
                        """

    query_series_popularity_genre = """
                        PREFIX serie:<http://moviesProject.org/sub/serie/>
                        PREFIX pred:<http://moviesProject.org/pred/>
                        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                        SELECT ?serie ?id ?poster ?title ?has_score ?popularity
                        WHERE 
                        {{
                        {{
                            ?serie pred:id_s ?id .
                            ?serie pred:poster ?poster .
                            ?serie pred:title ?title .
                            ?serie pred:has_score ?has_score .
                            ?serie pred:popularity ?popularity .
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
        return series(request, _filter, _order)

    elif request.POST.get('checkbox'):
        query_genre = """
                    PREFIX pred:<http://moviesProject.org/pred/> 
                        SELECT ?serie ?id ?poster ?title ?has_score
                        WHERE {{
                            ?serie pred:id_s ?id .
                            ?serie pred:poster ?poster .
                            ?serie pred:title ?title .
                            ?serie pred:has_score ?has_score .
                            {}
                        }}
                        """
        intersect_query_genre =  """
                                {{
                                        ?serie pred:id_s ?id .
                                        ?serie pred:poster ?poster .
                                        ?serie pred:title ?title .
                                        ?serie pred:has_score ?has_score .
                                        {}
                                }}
                                """
        if request.POST.get('order'):
            add_to_query = ""
            for filt in filter:
                add_to_query += '?serie pred:genre "{}" .\n'.format(str(filt))
            if order == "Average":    
                query = query_series_score_genre.format(add_to_query)
            elif order == "Popularity":
                query = query_series_popularity_genre.format(add_to_query)
            else:
                query = query_series_alphabetic_genre.format(add_to_query)
        else:
            add_to_query = ""
            for filt in filter:
                add_to_query += '?serie pred:genre "{}" .\n'.format(str(filt)) 
            query = query_genre.format(add_to_query)
    else:
        if request.POST.get('order'):
            myDict = dict(request.POST.lists())
            order = myDict['order'][0]
            if order == "Average":
                query = query_series_score
            elif order == "Popularity":
                query = query_series_popularity
            else:
                query = query_series_alphabetic
        else:
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

    sgenres = get_series_genres()

    if 'info-m' in request.POST:
        id = request.POST.get('info-m')
        detail_info(request, id)
        return HttpResponseRedirect('/info/' + id)

    tparams = {
        'series_all': series_all,
        'series_genres': sgenres,
    }

    return render(request, 'series_list.html', tparams)

def get_search_results(request, _str):
    if 'search' in request.POST:
        _str = request.POST.get('search', '')
        return HttpResponseRedirect('/search_results/' + _str)
    # if 'show_info' in request.POST:
    #     res = request.POST.get('show_info')
    #     res_div = res.split(",")
    #     if res_div[0] == "True":
    #         id = res_div[1]
    #     else:
    #         id = res_div[1] + ".s"
    #     detail_info(request, id)
    #     return HttpResponseRedirect('/info/' + id)
    query = """
        PREFIX predicate: <http://moviesProject.org/pred/>
        select ?name ?id ?id_m ?id_s ?title ?description ?poster ?score ?genre
        where 
        {{
            {{
                ?movie predicate:id_m ?id_m .
                ?movie predicate:title ?title . 
                ?movie predicate:description ?description .
                ?movie predicate:poster ?poster .
                ?movie predicate:has_score ?score .
                ?movie predicate:genre ?genre
                FILTER regex(?title, "{}")
            }}
            UNION
            {{
                ?movie predicate:id_m ?id_m .
                ?movie predicate:title ?title . 
                ?movie predicate:description ?description .
                ?movie predicate:poster ?poster .
                ?movie predicate:has_score ?score .
                ?movie predicate:genre ?genre
                FILTER regex(?description, "{}")
            }}
            UNION
            {{
                ?serie predicate:id_s ?id_s .
                ?serie predicate:title ?title .
                ?serie predicate:description ?description .
                ?serie predicate:poster ?poster .
                ?serie predicate:has_score ?score .
                ?serie predicate:genre ?genre
                FILTER regex(?title, "{}")
            }}
            UNION
            {{
                ?serie predicate:id_s ?id_s .
                ?serie predicate:title ?title .
                ?serie predicate:description ?description .
                ?serie predicate:poster ?poster .
                ?serie predicate:has_score ?score .
                ?serie predicate:genre ?genre
                FILTER regex(?description, "{}")
            }}
            UNION
            {{
                ?person predicate:id ?id .
                ?person predicate:name ?name .
                ?person predicate:popularity ?score 
                FILTER regex(?name, "{}")
            }}
        }}
            """.format(_str, _str, _str, _str, _str)
    # print(query)
    payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query,
                                 repo_name=repo_name)

    res = json.loads(res)
    movies_series_list = []
    cast_list = []
    # print(res)
    for e in res['results']['bindings']:
        movie_serie = []
        person = []
        genres = []
        if 'id_m' in e.keys():
            movie_serie.append(e['id_m']['value'])
            movie_serie.append(e['title']['value'])
            movie_serie.append(e['description']['value'])
            movie_serie.append(e['score']['value'])
            if 'poster' in e.keys():
                movie_serie.append(IMAGES_SITE + str(e['poster']['value']))
            else:
                movie_serie.append("None")
            if len(movies_series_list) == 0 or not movie_serie[0] in movies_series_list[len(movies_series_list)-1]:                    
                genres.append(e['genre']['value'])
                movie_serie.append(genres)
                movies_series_list.append(movie_serie)
            else:
                movies_series_list[len(movies_series_list)-1][5].append(e['genre']['value'])
        elif 'id_s' in e.keys():
            movie_serie.append(e['id_s']['value'])
            movie_serie.append(e['title']['value'])
            movie_serie.append(e['description']['value'])
            movie_serie.append(e['score']['value'])
            if 'poster' in e.keys():
                movie_serie.append(IMAGES_SITE + str(e['poster']['value']))
            else:
                movie_serie.append("None")
            if len(movies_series_list) == 0 or not movie_serie[0] in movies_series_list[len(movies_series_list)-1]:                    
                genres.append(e['genre']['value'])
                movie_serie.append(genres)
                movies_series_list.append(movie_serie)
            else:
                movies_series_list[len(movies_series_list)-1][5].append(e['genre']['value'])
        else:
            person.append(e['id']['value'])
            person.append(e['name']['value'])
            person.append(e['score']['value'])
            cast_list.append(person)

    for movie in movies_series_list:
        genre_str = ""
        for genre in movie[5]:
            genre_str+= "["+str(genre)+"]"
        movie[5] = genre_str

    tparams = {
        'str': _str,
        'result_movies_series': movies_series_list,
        'result_cast': cast_list,
    }

    return render(request, 'search_result.html', tparams)
    
def get_reviews(id):

    query = """
            PREFIX pred:<http://moviesProject.org/pred/>
            SELECT ?author ?content ?id
            WHERE{{
                {{
                    ?rev pred:is_from ?mov .
                    ?mov pred:id_m "{}" .
                    ?rev pred:content_is ?content .
                    ?rev pred:made_by ?author .
                    ?rev pred:id_r ?id .
                }}
                union
                {{
                    ?rev pred:is_from ?mov .
                    ?serie pred:id_s "{}" .
                    ?rev pred:content_is ?content .
                    ?rev pred:made_by ?author .
                    ?rev pred:id_r ?id .
                }}
            }}""".format(id, id)

    payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query,
                                 repo_name=repo_name)

    res = json.loads(res)
    reviews = []
    for e in res['results']['bindings']:
        for v in e.values():
            reviews.append(v['value'])

    return reviews

def detail_info(request, id):


    query = """
            PREFIX pred:<http://moviesProject.org/pred/>
            SELECT distinct ?id ?title ?poster ?pop ?score ?rel ?run ?genre ?des ?job ?char ?name ?ppop
            WHERE {{
                ?movie pred:id_m "{}" .
                ?movie pred:genre ?genre .
                ?movie pred:poster ?poster .
                ?movie pred:title ?title .
                ?movie pred:has_score ?score .
                ?movie pred:popularity ?pop .
                ?movie pred:runtime ?run .
                ?movie pred:released ?rel .
                ?movie pred:description ?des .
                optional{{
                    ?crew pred:takes_part ?movie .
                    ?crew pred:person ?person .
                    ?crew pred:job ?job .
                    ?person pred:name ?name .
                    ?person pred:popularity ?ppop .
                }}
                optional{{
                    ?crew pred:interpret ?char .
                }}
            }}""".format(id)

    payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query,
                                 repo_name=repo_name)

    res = json.loads(res)

    info_all = []
    info_all.append(res['results']['bindings'][0]['title']['value'])
    if str(res['results']['bindings'][0]['poster']['value']) is not "":
        poster = IMAGES_SITE + str(res['results']['bindings'][0]['poster']['value'])
    else:
        poster = NO_IMAGE
    info_all.append(poster)
    info_all.append(res['results']['bindings'][0]['pop']['value'])
    info_all.append(res['results']['bindings'][0]['score']['value'])
    info_all.append(res['results']['bindings'][0]['rel']['value'])
    info_all.append(res['results']['bindings'][0]['run']['value'])
    info_all.append(res['results']['bindings'][0]['genre']['value'])
    info_all.append(res['results']['bindings'][0]['des']['value'])
    for e in res['results']['bindings']:
        info_tmp = []
        #info_tmp.append(e['id']['value'])
        info_tmp.append(e['job']['value'])
        if 'char' in e.keys():
            info_tmp.append(e['char']['value'])
        info_tmp.append(e['name']['value'])
        #info_tmp.append(e['ppop']['value'])
        info_all.append(info_tmp)

    print(info_all)

    reviews = get_reviews(id)

    tparams = {
        'reviews': reviews,
        'result': info_all,
    }

    return render(request, 'info.html', tparams)


def playlist(request):
    if 'search' in request.POST:
        _str = request.POST.get('search', '')
        return HttpResponseRedirect('/search_results/' + _str)
    fav = get_top_movies()

    tparams = {
        'fav': fav,
    }

    return render(request, 'playlist.html', tparams)

def full_news(request):
    if 'search' in request.POST:
        _str = request.POST.get('search', '')
        return HttpResponseRedirect('/search_results/' + _str)
    return render(request, 'news.html')

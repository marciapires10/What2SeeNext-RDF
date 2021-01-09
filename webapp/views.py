import json
from webapp import queries
from django.http import HttpResponseRedirect
from django.shortcuts import render
from s4api.graphdb_api import GraphDBApi
from s4api.swagger import ApiClient
import random, string

IMAGES_SITE = "http://image.tmdb.org/t/p/w200"
NO_IMAGE = "../static/assets/img/NoImage.jpg"
PERSON_IMAGE = "../static/assets/img/person.jpeg"
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
        query = """
            PREFIX predicate: <http://moviesProject.org/pred/>
            ASK
            where 
            {{
                ?movie predicate:id_m "{}" .
            }}
            """.format(id)
        payload_query = {"query": query}
        res = accessor.sparql_select(body=payload_query,
                                    repo_name=repo_name)

        res = json.loads(res)
        is_movie = res['boolean']
        is_movie_str = ""
        if is_movie:
            is_movie_str = "movie"
        else:
            is_movie_str = "serie"
        detail_info(request, id, is_movie_str)
        return HttpResponseRedirect('/info/' + id + "/" + is_movie_str)

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
        detail_info(request, id, "movie")
        return HttpResponseRedirect('/info/' + id + "/" + "movie")
    
    if 'add-to-b' in request.POST:
        id = request.POST.get('add-to-b')
        add_movie_to_favList(id)

    tparams = {
        'movies_all': movies_all,
        'movie_genres': mgenres,
    }

    return render(request, 'movies_list.html', tparams)

def add_movie_to_favList(id):
    update = """
            PREFIX predicate: <http://moviesProject.org/pred/>
            PREFIX movie: <http://moviesProject.org/sub/mov/>
            PREFIX list: <http://moviesProject.org/sub/list/>
            INSERT DATA
            {{
                list:list_1
                    predicate:has movie:{} ;
                    predicate:name "list_1" .
            }}
            """.format(id)

    payload_query = {"update": update}
    res = accessor.sparql_update(body=payload_query,
                                repo_name=repo_name)
    return

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

    sgenres = get_series_genres()

    if 'info-m' in request.POST:
        id = request.POST.get('info-m')
        print("Vim pelas series")
        detail_info(request, id, "serie")
        return HttpResponseRedirect('/info/' + id + "/" + "serie")

    if 'add-to-b' in request.POST:
        print("Add Serie")
        id = request.POST.get('add-to-b')
        add_serie_to_favList(id)

    tparams = {
        'series_all': series_all,
        'series_genres': sgenres,
    }

    return render(request, 'series_list.html', tparams)

def add_serie_to_favList(id):
    update = """
            PREFIX predicate: <http://moviesProject.org/pred/>
            PREFIX serie: <http://moviesProject.org/sub/serie/>
            PREFIX list: <http://moviesProject.org/sub/list/>
            INSERT DATA
            {{
                list:list_1
                    predicate:has serie:{} ;
                    predicate:name "list_1" .
            }}
            """.format(id)
    payload_query = {"update": update}
    res = accessor.sparql_update(body=payload_query,
                                repo_name=repo_name)
    return

def get_search_results(request, _str):
    if 'search' in request.POST:
        _str = request.POST.get('search', '')
        return HttpResponseRedirect('/search_results/' + _str)

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
    payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query,
                                 repo_name=repo_name)

    res = json.loads(res)
    movies_series_list = []
    cast_list = []
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
            person.append(PERSON_IMAGE)
            cast_list.append(person)

    for movie in movies_series_list:
        genre_str = ""
        for genre in movie[5]:
            genre_str+= "["+str(genre)+"]"
        movie[5] = genre_str

    if 'info-m' in request.POST:
        id = request.POST.get('info-m')
        query = """
            PREFIX predicate: <http://moviesProject.org/pred/>
            ASK
            where 
            {{
                ?movie predicate:id_m "{}" .
            }}
            """.format(id)
        payload_query = {"query": query}
        res = accessor.sparql_select(body=payload_query,
                                    repo_name=repo_name)

        res = json.loads(res)
        is_movie = res['boolean']
        is_movie_str = ""
        if is_movie:
            is_movie_str = "movie"
        else:
            is_movie_str = "serie"
        detail_info(request, id, is_movie_str)
        return HttpResponseRedirect('/info/' + id + "/" + is_movie_str)

    tparams = {
        'str': _str,
        'result_movies_series': movies_series_list,
        'result_cast': cast_list,
    }

    return render(request, 'search_result.html', tparams)

def get_review_id():
    id_exists = True
    id_str = ""
    while id_exists:        
        id_str = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(24))

        query = """
                PREFIX predicate: <http://moviesProject.org/pred/>
                ASK
                where 
                {{
                    ?review predicate:id_r "{}" .
                }}
                """.format(id_str)
        payload_query = {"query": query}
        res = accessor.sparql_select(body=payload_query,
                                    repo_name=repo_name)

        res = json.loads(res)
        id_exists = res['boolean']

    return id_str

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
                    ?rev pred:is_from ?serie .
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
        review = []
        for v in e.values():
            review.append(v['value'])
        reviews.append(review)

    return reviews

def detail_info(request, id, is_movie = "movie"):
    if is_movie == "movie":
        query = """
                PREFIX pred:<http://moviesProject.org/pred/>
                SELECT distinct ?movie ?id ?title ?poster ?score ?rel ?run ?genre ?des ?id_p ?job ?char ?name ?ppop
                WHERE {{
                    ?movie pred:id_m "{}" .
                    ?movie pred:genre ?genre .
                    ?movie pred:poster ?poster .
                    ?movie pred:title ?title .
                    ?movie pred:has_score ?score .
                    ?movie pred:runtime ?run .
                    ?movie pred:released ?rel .
                    ?movie pred:description ?des .
                    optional{{
                        ?crew pred:takes_part ?movie .
                        ?crew pred:person ?person .
                        ?crew pred:job ?job .
                        ?person pred:id ?id_p .
                        ?person pred:name ?name .
                        ?person pred:popularity ?ppop .
                    }}
                    optional{{
                        ?crew pred:interpret ?char .
                    }}
                }}""".format(id)
    else:
        query = """
                PREFIX pred:<http://moviesProject.org/pred/>
                SELECT distinct ?serie ?id ?title ?poster ?score ?rel ?run ?genre ?des ?id_p ?job ?char ?name
                WHERE {{
                    ?serie pred:id_s "{}" .
                    ?serie pred:genre ?genre .
                    ?serie pred:poster ?poster .
                    ?serie pred:title ?title .
                    ?serie pred:has_score ?score .
                    ?serie pred:last_aired ?run .
                    ?serie pred:released ?rel .
                    ?serie pred:description ?des .
                    optional{{
                        ?crew pred:takes_part ?serie .
                        ?crew pred:person ?person .
                        ?crew pred:job ?job .
                        ?person pred:id ?id_p .
                        ?person pred:name ?name .
                    }}
                    optional{{
                        ?crew pred:interpret ?char .
                    }}
                }}""".format(id)

    payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query,
                                 repo_name=repo_name)

    res = json.loads(res)

    genres = []
    people = []
    for e in res['results']['bindings']:
        if len(people) == 0 or not e['id_p']['value'] in people[len(people)-1]:
            person = []
            person.append(e['id_p']['value'])
            person.append(e['job']['value'])
            person.append(e['name']['value'])
            if 'char' in e.keys():
                person.append(e['char']['value'])
            people.append(person)
        if not e['genre']['value'] in genres:
            genres.append(e['genre']['value'])
    
    genre_str = ""
    for genre in genres:
        genre_str += "[" + genre + "]"

    info_all = []
    if is_movie == "movie":
        info_all.append(res['results']['bindings'][0]['movie']['value'])
    else:
        info_all.append(res['results']['bindings'][0]['serie']['value'])
    info_all.append(res['results']['bindings'][0]['title']['value'])
    if str(res['results']['bindings'][0]['poster']['value']) is not "":
        poster = IMAGES_SITE + str(res['results']['bindings'][0]['poster']['value'])
    else:
        poster = NO_IMAGE
    info_all.append(poster)
    info_all.append(res['results']['bindings'][0]['score']['value'])
    info_all.append(res['results']['bindings'][0]['rel']['value'])
    info_all.append(res['results']['bindings'][0]['run']['value'])
    info_all.append(genre_str)
    info_all.append(res['results']['bindings'][0]['des']['value'])

    cast = ""
    crew = ""
    cast_counter= 0
    for person in people:
        if len(person) > 3:
            cast +="[" + str(person[2]) + " as '" + str(person[3]) + "'] "
        elif cast_counter < 10:
            crew +="[" + str(person[2]) + " works as '" + str(person[1]) + "'] "
            cast_counter += 1

    # print(cast)
    info_all.append(cast)
    info_all.append(crew)
    reviews = get_reviews(id)
    print(info_all)

    # delete review
    if request.POST.get('delete'):
        review_id = request.POST.get('delete')
        query = """
                PREFIX predicate: <http://moviesProject.org/pred/>
                DELETE {{?s ?p ?o}}
                WHERE{{ 
                    ?s predicate:id_r "{}".
                    ?s ?p ?o
                }}""".format(review_id)

        payload_query = {"update": query}
        res = accessor.sparql_update(body=payload_query,
                                    repo_name=repo_name)
        return HttpResponseRedirect('/info/' + id + "/" + is_movie)

    # add new review
    if request.POST.get('username') and request.POST.get('comment'):
        username = request.POST.get('username')
        comment = request.POST.get('comment').replace('"',"'")
        review_id = get_review_id()
        if is_movie == "movie":
            print("MOVIE")
            update = """
                    PREFIX pred:<http://moviesProject.org/pred/>
                    PREFIX fb: <http://rdf.freebase.com/ns/>
                    PREFIX review: <http://moviesProject.org/sub/review/>
                    PREFIX predicate: <http://moviesProject.org/pred/>
                    PREFIX movie: <http://moviesProject.org/sub/mov/>
                    INSERT DATA
                    {{ 
                        review:{}
                        predicate:id_r "{}";
                        predicate:made_by "{}";
                        predicate:content_is "{}";
                        predicate:is_from movie:{}.
                    }}""".format(review_id, review_id, username, comment, id)
        else:
            update = """
                    PREFIX pred:<http://moviesProject.org/pred/>
                    PREFIX fb: <http://rdf.freebase.com/ns/>
                    PREFIX review: <http://moviesProject.org/sub/review/>
                    PREFIX predicate: <http://moviesProject.org/pred/>
                    PREFIX serie: <http://moviesProject.org/sub/serie/>
                    INSERT DATA
                    {{ 
                        review:{}
                        predicate:id_r "{}" .
                        predicate:made_by "{}" .
                        predicate:content_is "{}".
                        predicate:is_from serie:{}.
                    }}""".format(review_id, review_id, username, comment, id)
        payload_query = {"update": update}
        res = accessor.sparql_update(body=payload_query,
                                    repo_name=repo_name)
        print(res)
        return HttpResponseRedirect('/info/' + id + "/" + is_movie)

    info_all_dict = []
    info_all_dict.append(info_all)
    tparams = {
        'reviews': reviews,
        'result': info_all_dict,
    }

    return render(request, 'info.html', tparams)

def film_by_year(request):
    query = """
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            select ?mov ?name ?runtime
            where {{
                SERVICE <https://dbpedia.org/sparql>{{
                    select ?name ?runtime where{{
                        ?mov dct:subject <http://dbpedia.org/resource/Category:{}_films> .
                        ?mov foaf:name ?name .
                        ?mov dbo:Work/runtime ?runtime .
                    }}
                }} 
            }}
            """.format(1999)
    payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
    print(res)
    res = json.loads(res)
    year_movies_list = []
    for e in res['results']['bindings']:
        movie = []
        movie.append(e['mov']['value'])
        movie.append(e['name']['value'])
        movie.append(e['runtime']['value'])
        year_movies_list.append(movie)

    tparams = {
        'year_movies': year_movies_list,
    }

    return render(request, 'news.html', tparams)

def film_from_dbpedia(request, mov_name):
    query = """
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        select ?title ?rel ?abs ?runtime ?pname ?dirname ?prodname
        where {
            SERVICE <https://dbpedia.org/sparql>{
                select ?title ?rel ?abs ?runtime ?pname ?dirname ?prodname{
                    <http://dbpedia.org/resource/{}> dbo:abstract ?abs .
                    <http://dbpedia.org/resource/{}> dbo:releaseDate ?rel .
                    <http://dbpedia.org/resource/{}> dbo:Work/runtime ?runtime .
                    <http://dbpedia.org/resource/{}> dbp:name ?title.
                }optional{
                    <http://dbpedia.org/resource/{}> dbo:starring ?starr.
                    <http://dbpedia.org/resource/{}> dbo:director ?dir .
                    ?dir dbp:name ?dirname .
                    <http://dbpedia.org/resource/{}> dbo:producer ?prod .
                    ?prod dbp:name ?prodname .
                    ?starr dbp:name ?pname .
                }
            } 
        }
    """.format(mov_name, mov_name, mov_name, mov_name, mov_name, mov_name, mov_name)
    payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
    res = json.loads(res)
    movie_info = []
    for e in res['results']['bindings']:
        info = []
        info.append(e['title']['value'])
        info.append(e['rel']['value'])
        info.append(e['abs']['value'])
        info.append(e['runtime']['value'])
        if "prodname" and "pname" and "dirname" in e.keys():
            info.append(e['pname']['value'])
            info.append(e['dirname']['value'])
            info.append(e['prodname']['value'])
        movie_info.append(info)

    tparams = {
        'mov_info': movie_info,
    }

    return render(request, 'news.html', tparams)

def playlist(request):
    if 'search' in request.POST:
        _str = request.POST.get('search', '')
        return HttpResponseRedirect('/search_results/' + _str)

    query = """
            PREFIX predicate: <http://moviesProject.org/pred/>
            PREFIX movie: <http://moviesProject.org/sub/mov/>
            PREFIX list: <http://moviesProject.org/sub/list/>
            SELECT DISTINCT ?id ?title ?poster ?score
            WHERE
            { 
                {
                list:list_1 predicate:has ?movie .
                ?movie predicate:id_m ?id .
                ?movie predicate:title ?title .
                ?movie predicate:poster ?poster .
                ?movie predicate:has_score ?score .
                }
                UNION
                {
                list:list_1 predicate:has ?serie .
                ?serie predicate:id_s ?id .
                ?serie predicate:title ?title .
                ?serie predicate:poster ?poster .
                ?serie predicate:has_score ?score .
                }
            }
            """

    payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
    res = json.loads(res)
    fav = []
    for e in res['results']['bindings']:
        movie = []
        movie.append(e['id']['value'])
        movie.append(e['title']['value'])
        if 'poster' in e.keys():
            movie.append(IMAGES_SITE + str(e['poster']['value']))
        else:
            movie.append(NO_IMAGE)
        movie.append(e['score']['value'])
        fav.append(movie)

    tparams = {
        'fav': fav,
    }

    return render(request, 'playlist.html', tparams)

def full_news(request):
    if 'search' in request.POST:
        _str = request.POST.get('search', '')
        return HttpResponseRedirect('/search_results/' + _str)
    return render(request, 'news.html')

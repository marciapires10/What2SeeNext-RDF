top_10_movies = """
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


top_10_series = """
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

get_genres = """
            PREFIX pred:<http://moviesProject.org/pred/>
            SELECT DISTINCT ?genre_m
            WHERE {
                ?movie pred:genre ?genre_m .
            }
            ORDER BY ASC(?genre_m)
            """

all_movies = """
            PREFIX mov:<http://moviesProject.org/sub/mov/>
            PREFIX pred:<http://moviesProject.org/pred/>
            SELECT ?movie ?id ?poster ?title
            WHERE {
                ?movie pred:id_m ?id .
                ?movie pred:poster ?poster .
                ?movie pred:title ?title .
            }"""

all_series = """
            PREFIX pred:<http://moviesProject.org/pred/>
            SELECT ?id ?poster ?title
            WHERE {
                ?serie pred:id_s ?id .
                ?serie pred:poster ?poster .
                ?serie pred:title ?title .
            }"""

order_movies_popularity = """
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

order_movies_score = """
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

order_movies_alphabetic = """
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

movie_by_genre =  """
                    PREFIX pred:<http://moviesProject.org/pred/> 
                        SELECT ?movie ?id ?poster ?title ?has_score
                        WHERE {{
                            ?movie pred:id_m ?id .
                            ?movie pred:poster ?poster .
                            ?movie pred:title ?title .
                            ?movie pred:has_score ?has_score .
                            ?movie pred:genre "{}" .
                        }}
                        """
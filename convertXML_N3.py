from lxml import etree


XML_FILE_MOVIES = "Files/movies.xml"
XML_FILE_REVIEWS = "Files/reviews.xml"
XML_FILE_CAST = "Files/casts.xml"

def create_cast():
    cast_n3 = open("cast.n3", "w")
    
    cast_n3.write('@prefix movie: <http://moviesProject.org/sub/mov/>.\n')
    cast_n3.write('@prefix crew: <http://moviesProject.org/sub/crew/>.\n')
    cast_n3.write('@prefix person: <http://moviesProject.org/sub/person/>.\n')
    cast_n3.write('@prefix review: <http://moviesProject.org/sub/review/>.\n')
    cast_n3.write('@prefix predicate: <http://moviesProject.org/pred/>.\n')
    cast_n3.write('\n')

    el = etree.parse(XML_FILE_CAST)
    casts = el.xpath("//cast")

    person_id_found = []

    crews = []  # [[person_name, job, character]]

    for movie in casts:
        movie_id = ""
        if not movie.find("id") is None and not movie.find("id").text is None:
            movie_id = movie.find("id").text
        if not movie.find("cast") is None:
            for cast in movie.find("cast"):
                job = ""
                _id = ""
                is_adult = ""
                gender = ""
                name = ""
                popularity = ""
                char_name = ""

                if not cast.find("id") is None and not cast.find("id").text is None:    
                    # Crew
                    _id = cast.find("id").text
                    if not cast.find("character") is None and not cast.find("character").text is None:
                        char_name = cast.find("character").text.replace('"',"'")
                    if not cast.find("name") is None and not cast.find("name").text is None:
                            name = cast.find("name").text.replace('"',"'")
                    if not cast.find("known_for_department") is None and not cast.find("known_for_department").text is None:
                            job = cast.find("known_for_department").text
                    # Person, check if already exists
                    if not cast.find("id").text in person_id_found:
                        _id = cast.find("id").text
                        person_id_found.append(_id)
                        if not cast.find("gender") is None and not cast.find("gender").text is None:
                            gender = cast.find("gender").text
                        if not cast.find("adult") is None and not cast.find("adult").text is None:
                            is_adult = cast.find("adult").text
                        if not cast.find("popularity") is None and not cast.find("popularity").text is None:
                            popularity = cast.find("popularity").text

                        cast_n3.write("person:"+ _id + "\n")
                        cast_n3.write('\tpredicate:id "' + _id + '";\n')
                        cast_n3.write('\tpredicate:name "' + name + '";\n')
                        cast_n3.write('\tpredicate:popularity "' + popularity + '";\n')
                        cast_n3.write('\tpredicate:gender "' + gender + '";\n')
                        cast_n3.write('\tpredicate:is_adult "' + is_adult + '".\n')
                        
                    crew = []
                    crew.append(_id)
                    crew.append(job)
                    crew.append(char_name)
                    crew.append(movie_id)
                    crews.append(crew)

            for crew in movie.find("crew"):
                job = ""
                _id = ""
                is_adult = ""
                gender = ""
                name = ""
                popularity = ""
                char_name = ""

                if not crew.find("id") is None and not crew.find("id").text is None:    
                    # Crew
                    _id = crew.find("id").text
                    if not crew.find("known_for_department") is None and not crew.find("known_for_department").text is None:
                            job = crew.find("known_for_department").text
                    # Person, check if already exists
                    if not _id in person_id_found:
                        person_id_found.append(_id)
                        if not crew.find("gender") is None and not crew.find("gender").text is None:
                            gender = crew.find("gender").text
                        if not crew.find("adult") is None and not crew.find("adult").text is None:
                            is_adult = crew.find("adult").text
                        if not crew.find("popularity") is None and not crew.find("popularity").text is None:
                            popularity = crew.find("popularity").text
                        if not crew.find("name") is None and not crew.find("name").text is None:
                            name = crew.find("name").text.replace('"',"'")

                        cast_n3.write("person:"+ _id + "\n")
                        cast_n3.write('\tpredicate:id "' + _id + '";\n')
                        cast_n3.write('\tpredicate:name "' + name + '";\n')
                        cast_n3.write('\tpredicate:popularity "' + popularity + '";\n')
                        cast_n3.write('\tpredicate:gender "' + gender + '";\n')
                        cast_n3.write('\tpredicate:is_adult "' + is_adult + '".\n')
                        
                    _crew = []
                    _crew.append(_id)
                    _crew.append(job)
                    _crew.append(None)
                    _crew.append(movie_id)
                    crews.append(_crew)
    
    for person in crews:
        cast_n3.write("crew:"+ person[0] + "\n")
        cast_n3.write('\tpredicate:job "' + person[1] + '";\n')
        if not person[2] is None:
            cast_n3.write('\tpredicate:interpret "' + person[2] + '";\n')
        cast_n3.write('\tpredicate:person person:' + person[0] + ';\n')
        cast_n3.write('\tpredicate:takes_part movie:' + person[3] + '.\n')

    cast_n3.close()

def create_review():
    reviews_n3 = open("reviews.n3", "w")

    #Initialize reviews_n3
    reviews_n3.write('@prefix movie: <http://moviesProject.org/sub/mov/>.\n')
    reviews_n3.write('@prefix crew: <http://moviesProject.org/sub/crew/>.\n')
    reviews_n3.write('@prefix person: <http://moviesProject.org/sub/person/>.\n')
    reviews_n3.write('@prefix review: <http://moviesProject.org/sub/review/>.\n')
    reviews_n3.write('@prefix predicate: <http://moviesProject.org/pred/>.\n')

    reviews_n3.write('\n')
    el = etree.parse(XML_FILE_REVIEWS)
    reviews = el.xpath("//review")

    for movie in reviews:
        reviews = [] # [[id, author, content]]
        movie_id = ""
        if not movie.find("id") is None and not movie.find("id").text is None:
            movie_id = movie.find("id").text

        if not movie.find("results") is None:
            for review in movie.find("results"):
                if not review.find("author") is None and not review.find("content") is None and not review.find("id") is None and not review.find("author").text is None and not review.find("content").text is None and not review.find("id").text is None:
                    _id = review.find("id").text
                    author = review.find("author").text
                    content = review.find("content").text.replace('"',"'")
                    review = []
                    review.append(_id) 
                    review.append(author)
                    review.append(content.replace("\n",""))
                    reviews.append(review)

        for review in reviews:
            reviews_n3.write("review:"+ review[0] + "\n")
        #Predicate and object
            reviews_n3.write('\tpredicate:made_by "' + review[1] + '";\n')
            reviews_n3.write('\tpredicate:content_is "' + review[2] + '";\n')
            reviews_n3.write('\tpredicate:is_from movie:' + movie_id + '.\n')
    
    reviews_n3.close()

def create_movies():
    movies_n3 = open("movies.n3", "w")

    #Initialize movies_n3
    movies_n3.write('@prefix movie: <http://moviesProject.org/sub/mov/>.\n')
    movies_n3.write('@prefix crew: <http://moviesProject.org/sub/crew/>.\n')
    movies_n3.write('@prefix person: <http://moviesProject.org/sub/person/>.\n')
    movies_n3.write('@prefix review: <http://moviesProject.org/sub/review/>.\n')
    movies_n3.write('@prefix predicate: <http://moviesProject.org/pred/>.\n')
    movies_n3.write('\n')
    # #Genres
    # movies_n3.write('genres:drama predicate:genre "Drama".\n')
    # movies_n3.write('genres:comedy predicate:genre "Comedy".\n')
    # movies_n3.write('genres:animation predicate:genre "Animation".\n')
    # movies_n3.write('genres:action_&_adventure predicate:genre "Action & Adventure".\n')
    # movies_n3.write('genres:crime predicate:genre "Crime".\n')
    # movies_n3.write('genres:historical predicate:genre "Historical".\n')
    # movies_n3.write('genres:horror predicate:genre "Horror".\n')
    # movies_n3.write('genres:mystery predicate:genre "Mystery".\n')
    # movies_n3.write('genres:political predicate:genre "Political".\n')
    # movies_n3.write('genres:romance predicate:genre "Romance".\n')
    # movies_n3.write('genres:sci_fi predicate:genre "Sci-Fi & Fantasy".\n')
    # movies_n3.write('genres:thriller predicate:genre "Thriller".\n')
    # movies_n3.write('genres:documentary predicate:genre "Documentary".\n')
    # movies_n3.write('genres:family predicate:genre "Family".\n')
    # movies_n3.write('genres:news predicate:genre "News".\n')
    # movies_n3.write('genres:reality predicate:genre "Reality".\n')
    # movies_n3.write('genres:soap predicate:genre "Soap".\n')
    # movies_n3.write('genres:talk predicate:genre "Talk".\n')
    # movies_n3.write('genres:kids predicate:genre "Kids".\n')
    # movies_n3.write('genres:politics predicate:genre "War & Politics".\n')
    # movies_n3.write('genres:music predicate:genre "Music".\n')
    # movies_n3.write('genres:war predicate:genre "War".\n')
    # movies_n3.write('genres:history predicate:genre "History".\n')
    # movies_n3.write('genres:western predicate:genre "Western".\n')
    # movies_n3.write('genres:tv_movie predicate:genre "TV Movie".\n')

    # Languages
    el = etree.parse(XML_FILE_MOVIES)
    movies = el.xpath("//movie")
    for movie in movies:
        # Initialize
        _id = ""
        is_adult = ""
        genres = []
        languages = []
        overview = ""
        popularity = ""
        poster_path = ""
        release_date = ""
        runtime = ""
        vote_average = ""
        title = ""
        _str = ""
        print("\n\n--------------- New Movie ------------------")
        if not movie.find("id") is None and not movie.find("id").text is None:
            _id = movie.find("id").text
            _str += _id + ";"
        if not movie.find("adult") is None and not movie.find("adult").text is None:
            is_adult = movie.find("adult").text
            _str += is_adult + ";"
        if not movie.find("overview") is None and not movie.find("overview").text is None:
            overview = movie.find("overview").text.replace('"',"'")
            _str += overview + ";"
        if not movie.find("popularity") is None and not movie.find("popularity").text is None:
            popularity = movie.find("popularity").text
            _str += popularity + ";"
        if not movie.find("poster_path") is None and not movie.find("poster_path").text is None:
            poster_path = movie.find("poster_path").text
            _str += poster_path + ";"
        if not movie.find("release_date") is None and not movie.find("release_date").text is None:
            release_date = movie.find("release_date").text
            _str += release_date + ";"
        if not movie.find("runtime") is None and not movie.find("runtime").text is None:
            runtime = movie.find("runtime").text
            _str += runtime + ";"
        if not movie.find("vote_average") is None and not movie.find("vote_average").text is None:
            vote_average = movie.find("vote_average").text
            _str += vote_average + ";"
        if not movie.find("title") is None and not movie.find("title").text is None:
            title = movie.find("title").text
            _str += title + ";"
        if not movie.find("genres") is None:
            for genre in movie.find("genres"):
                if not genre.find("name") is None and not genre.find("name").text is None:
                    genres.append(genre.find("name").text)
                    _str += genre.find("name").text + ";"
        if not movie.find("spoken_languages") is None:
            for language in movie.find("spoken_languages"):
                if not language.find("name") is None and not language.find("name").text is None:
                    languages.append(language.find("name").text)
                    _str += language.find("name").text + ";"

        #Subject
        _title = title.replace(" ", "_").lower()
        # movies_n3.write("movie:"+ _title + "\n")
        movies_n3.write("movie:"+ _id + "\n")
        #Predicate and object
        movies_n3.write('\tpredicate:id "' + _id + '";\n')
        movies_n3.write('\tpredicate:title "' + title + '";\n')
        movies_n3.write('\tpredicate:description "' + overview + '";\n')
        movies_n3.write('\tpredicate:popularity "' + popularity + '";\n')
        movies_n3.write('\tpredicate:has_score "' + vote_average + '";\n')
        movies_n3.write('\tpredicate:released "' + release_date + '";\n')
        movies_n3.write('\tpredicate:poster "' + poster_path + '";\n')
        for genre in genres:
            movies_n3.write('\tpredicate:genre "' + genre + '";\n')
        for language in languages:
            movies_n3.write('\tpredicate:language "' + language + '";\n')
        movies_n3.write('\tpredicate:runtime "' + runtime + '".\n')

    movies_n3.close()

def main():
    create_movies()
    create_review()
    create_cast()

if __name__ == "__main__":
    main()

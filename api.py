from flask import Flask, make_response, jsonify, request
import dataset
import requests
import os


app = Flask(__name__)
db = dataset.connect('sqlite:///api.db')
API_KEY = os.environ.get("API_KEY")
table = db['movies']

def fetch_db(movie_id):
    # Each movie scnerio
    return table.find_one(id=movie_id)


def fetch_db_all():
    # For All movies dictionaries
    movies = []
    for movie in table:
        movies.append(movie)
    return movies


@app.route('/api/search_movies/<title>', methods=['GET'])
def api_searched_movies(title):
    '''
    GET request to /api/search_movie returns the movies with specific title
    '''

    movies_data=fetch_db_all()
    search_movie={}
    for i in range(0,len(movies_data)):
        dic=dict(movies_data[i])
        if dic.get("title")==title.title():
            search_movie=dic
            break
    return make_response(jsonify(search_movie), 200)

@app.route('/api/movies', methods=['GET', 'POST'])
def api_movies():
    '''
    GET : request to /api/movies returns the details of all movies in database,
    POST : fetch data from "http://www.omdbapi.com/" and Store  date in database ,
    '''
    if request.method == "GET":
        return make_response(jsonify(fetch_db_all()), 200)
    elif request.method == 'POST':
        content = request.json
        title=content.get("title")
        movies_data=fetch_db_all()
        found=False
        for i in range(0,len(movies_data)):
            dic=dict(movies_data[i])
            if dic.get("title")==title.title():
                found=True
                break
        if found:
            message={"error":"already exist in list"}
            return make_response(jsonify(message), 404)
        response = requests.get(f"http://www.omdbapi.com/?t={title}&apikey={API_KEY}").json()
        thumbnails=response.get('Poster')
        movie_name=response.get('Title')
        genre=response.get('Genre')
        cast=response.get('Actors')
        director=response.get('Director')
        res={'title':movie_name,
        'thumbnails':thumbnails,
        'genre':genre,
        'cast':cast,
        'director':director}
        movie_name = content['title']
        table.insert(res)
        return make_response(jsonify(res), 201)

@app.route('/api/movies/<movie_id>', methods=['GET', 'PUT'])
def api_each_movie(movie_id):
    '''
    GET : request to /api/movies/<movie_id> returns the details of a movie from database,
    PUT : request to /api/movies/<movie_id> update the movie in database,
    '''
    if request.method == "GET":
        movie_obj = fetch_db(movie_id)
        if movie_obj:
            return make_response(jsonify(movie_obj), 200)
        if not movie_obj:
            message={"error":"Movie doesn't exist with id {}".format(movie_id)}
            return make_response(jsonify(message), 404)
    elif request.method == "PUT":  # Updates the movie
        content = request.json
        table.update(content, ['id'])

        movies_obj = fetch_db(movie_id)
        return make_response(jsonify(movies_obj), 200)

@app.route('/api/<director>', methods=['GET'])
def api_director(director):
    '''
    GET : request to /api/<director> returns the director with movies list    
    '''
    movie_data=fetch_db_all()
    director_movie={}
    movie_list=[]
    for i in range(0,len(movie_data)):
        dic=dict(movie_data[i])
        director_movie[director]=director
        if dic.get("director") is None:
            continue 
        if director in dic.get("director"):
            movie_list.append(dic.get("title"))
            
    director_movie["movies_list"]=movie_list
    message={"Director with the name {}".format(director):director_movie}
    return make_response(jsonify(message), 200)

@app.route('/api/genre/<genre>', methods=['GET'])
def api_genre(genre):
    '''
    GET : request to /api/genre/<genre> returns the movie list with given genre
    '''
    movie_data=fetch_db_all()
    genre_movie={}
    movie_list=[]
    for i in range(0,len(movie_data)):
        dic=dict(movie_data[i])
        genre_movie[genre]=genre
        if dic.get("genre") is None:
            continue 
        if genre in dic.get("genre"):
            movie_list.append(dic.get("title"))
            
    genre_movie["movies_list"]=movie_list
    message={"Movies with the genre {}".format(genre):genre_movie}
    return make_response(jsonify(message), 200)

@app.route('/api/cast/<cast>', methods=['GET'])
def api_cast(cast):
    '''
    GET : request to /api/cast/<cast> returns the movies list with given cast,
    '''
    movie_data=fetch_db_all()
    genre_movie={}
    movie_list=[]
    cast=cast.title()
    cast_list=[]
    for i in range(0,len(movie_data)):
        dic=dict(movie_data[i])        
        if dic.get("cast") is None:
            continue
        if cast in dic.get('cast'):
            cast_list.append(cast) 
        if cast in dic.get("cast"):
            movie_list.append(dic.get("title"))
    cast_list=list(set(cast_list))
    genre_movie['cast']=cast_list     
    genre_movie["movies_list"]=movie_list
    message={"Cast with the Movies {}".format(cast):genre_movie}
    return make_response(jsonify(message), 200)


if __name__ == '__main__':
    app.run(debug=True)

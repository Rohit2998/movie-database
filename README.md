# STEPS TO RUN All API Requests


Install requirements.txt packages


# create .env file
*paste API_KEY = dfe957a3

# Run flask app
using command 
-- python .\api.py

# Api Contracts used:

POST
http://127.0.0.1:5000/api/movies

GET
http://127.0.0.1:5000/api/movies

GET 
http://127.0.0.1:5000/api/search_movies/<movie_name>

GET
http://127.0.0.1:5000/api/movies/<movie_id>

GET 
http://127.0.0.1:5000/api/<director_name>

GET 
http://127.0.0.1:5000/api/genre/<genre>

GET 
http://127.0.0.1:5000/api/cast/<cast_name>
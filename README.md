# Final Project

## Casting Agency App

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors, writers and directors to those movies. Users can define, list, delete and search the movies and participance according to their roles.

The application can:

1. Create/delete movies.
2. Create/delete persons.
2. Create/delete participances.
3. Search for movies and persons based on a text query string.
4. Roles and permission are configured in Auth0.

## Getting started

### Pre-requisites and Local Development 

Developers using this project should already have Python3 and pip installed on their local machines. Developers should also be able to create postgres databases on their local machines.

1. Clone the repository.
```
git clone ...
cd ...
```
2. Create a virtual environment:
```
python3 venv env
```

3. Install dependencies:
```
./env/bin/pip install -r ./requirements.txt
```
4. Configure for local development.
*Create Development and Test Postgres Databases*
```
createdb castagency_test
createdb castagency
```

Copy `config_template.py` as `config.py` and `test_config.py`. Then edit these files with secret information.*

5. Execute `setup.sh` to create initial data.
```
./setup.sh
```

6. Use your favourite IDE to execute `app.py`.

Authentication: This application require authentication configured in Auth0. 
Authentication roles: 
 - Casting Assistant : Can view actors and movies.
 - Casting Director : All permissions a Casting Assistant has and add or delete an actor from the database, modify actors or movies.
 - Executive Producer : All permissions a Casting Director has and add or delete a movie from the database.

All required configuration settings and roles token's are included in a bash file which is `config.py`

## Error Handling

Errors are returned as JSON objects in the following format

```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 401: Authorization Error
- 404: Resource Not Found
- 422: Not Processable 
- 500: Internal Server Error

## Testing

tests for the success and error behavior of each endpoint using the unittest library, configured in `test_config.py`

## Endpoint Library

`GET /movies`

General : Returns movies in a dictionary objects including movies in a list including name, genres, release_date, total count and success value. 

Sample: 
curl --location 'http://127.0.0.1:8080/movies?page=2' \
    --header 'Authorization: Bearer '

Returns:
```json
{
    "movies": [
        {
            "genre": [
                "Crime",
                "Drama"
            ],
            "id": 5,
            "name": "The Godfather",
            "release_date": "Wed, 21 Oct 1970 00:00:00 GMT"
        }
    ],
    "success": true,
    "total_count": 3
}
```


`GET /movies/3`

General : Returns movie in a dictionary objects including success value, movie id, name , release date and movie's participances in a list including names and missions. 

Sample: 

curl --location 'http://127.0.0.1:8080/movies/3' \
    --header 'Authorization: Bearer '

Returns:
```json
{
    "genre": [
        "Crime",
        "Drama"
    ],
    "id": 5,
    "name": "The Godfather",
    "participances": [
        {
            "mission": "Star",
            "name": "Al Pacino"
        },
        {
            "mission": "Director",
            "name": "Francis Ford Coppola"
        }
    ],
    "release_date": "Thu, 21 Oct 1965 00:00:00 GMT",
    "success": true
}
```

`GET /persons`

General : Returns persons in a dictionary objects including movies in a list including id, name, gender, participances, birth_date, total count and success value. 

Sample: 

curl --location 'http://127.0.0.1:8080/persons?page=10' \
    --header 'Authorization: Bearer '

Returns:
```json
{
"persons": [
        {
            "birth_date": "Fri, 08 May 2020 00:00:00 GMT",
            "gender": "{Male}",
            "id": 4,
            "name": "Poyraz Haspulat",
            "participances": [
                "Writer",
                "Star"
            ]
        },
        {
            "birth_date": "Sun, 25 Apr 1920 00:00:00 GMT",
            "gender": "Male",
            "id": 6,
            "name": "Al Pacino",
            "participances": [
                "Star"
            ]
        }
    ],
    "success": true,
    "total_count": 5
}
```

`GET /participances`

General : Returns participances in a dictionary objects including mission, movie and person description in a list, total count and success value. 

Sample: 

curl --location 'http://127.0.0.1:8080/participances?page=2' \
    --header 'Authorization: Bearer '

Returns:
```json
{
    "participances": [
        {
            "mission": {
                "id": 2,
                "name": "Writer"
            },
            "movie": {
                "id": 3,
                "name": "Avatar"
            },
            "person": {
                "id": 4,
                "name": "James Cameron"
            }
        },
        {
            "mission": {
                "id": 3,
                "name": "Star"
            },
            "movie": {
                "id": 5,
                "name": "The Godfather"
            },
            "person": {
                "id": 6,
                "name": "Al Pacino"
            }
        }
    ],
    "success": true,
    "total_count": 6
}
```

`POST /participances`

General: Sends a post request in order to add a new participance which is including person, movie and mission description.

Sample:

curl --location 'http://127.0.0.1:8080/participances' \
    --header 'Authorization: Bearer ' \
    --header 'Content-Type: application/json' \
    --data '{"participance":{"person_id":"8","movie_id":"3","mission_id":"2"}}'

Returns: 
```json
{
    "id": 11,
    "success": true
}
```

`POST /movies`

General: Sends a post request in order to add a new movie.

Sample: 

curl --location 'http://127.0.0.1:8080/movies' \
--header 'Authorization: Bearer ' \
--header 'Content-Type: application/json' \
--data '{"movie":{"name":"The Godfather","genre":["Crime","Drama"],"release_date":"10.21.1973"}}'

Returns: 
```json
{
    "id": 8,
    "success": true
}
```

`POST /movies`

General: Sends a post request in order to search for a specific movie name by search term in request body.

Sample: 

curl --location 'http://127.0.0.1:8080/movies' \
    --header 'Authorization: Bearer ' \
    --header 'Content-Type: application/json' \
    --data ' {"searchTerm":"TitaNi"}'

Returns: 
```json
{
    "movies": [
        {
            "name": "Titanic"
        }
    ],
    "total_movies": 1
}
```

`POST /persons`

General: Sends a post request in order to add a new person.

Sample:

curl --location 'http://127.0.0.1:8080/persons' \
        --header 'Authorization: Bearer ' \
        --header 'Content-Type: application/json' \
        --data '{"person":{"name":"Katee Sackhoff",
                                    "birth_date":"08-05-1980",
                                    "gender":"Female"}}'

Returns: 
```json
{
    "id": 11,
    "success": true
}
```

`POST /persons`

General: Sends a post request in order to search for a specific person name by search term in request body.

Sample:

curl --location 'http://127.0.0.1:8080/persons' \
--header 'Authorization: Bearer ' \
--header 'Content-Type: application/json' \
--data ' {"searchTerm":"SAck"}'

Returns: 
```json
{
    "persons": [
        {
            "name": "Katee Sackhoff"
        }
    ],
    "total_persons": 1
}
```

`DELETE /movies/${id}`

General: Deletes a specified movie using the`id` of the movie in request arguments.

Sample:

curl --location --request DELETE 'http://127.0.0.1:8080/movies/7' \
    --header 'Authorization: Bearer ' 

Returns: 
```json
{
    "id": 7,
    "success": true
}
```

`DELETE /persons/${id}`

General: Deletes a specified person using the`id` of the person in request arguments.

Sample:

curl --location --request DELETE 'http://127.0.0.1:8080/persons/10' \
    --header 'Authorization: Bearer ' 

Returns: 
```json
{
    "id": 10,
    "success": true
}
```


`PATCH /persons/${id}`

General: Sends a patch request in order to update release_date with a specified person using the `id` of request arguments 

Sample:

curl --location --request PATCH 'http://127.0.0.1:8080/persons/6' \
    --header 'Authorization: Bearer ' \
    --header 'Content-Type: application/json' \
    --data '{"person":{"birth_date":"04.25.1920"}}'

Returns: 
```json
{
    "success": true
}
```

`PATCH /persons/${id}`

General: Sends a patch request in order to update birth date with a specified person using the `id` of request arguments 

Sample:

curl --location --request PATCH 'http://127.0.0.1:8080/persons/6' \
    --header 'Authorization: Bearer ' \
    --header 'Content-Type: application/json' \
    --data '{"person":{"birth_date":"04.25.1920"}}'

Returns: 
```json
{
    "success": true
}
```

`PATCH /movies/${id}`

General: Sends a patch request in order to update release date with a specified movie using the `id` of request arguments.

Sample:

curl --location --request PATCH 'http://127.0.0.1:8080/movies/5' \
    --header 'Authorization: Bearer ' \
    --header 'Content-Type: application/json' \
    --data '{"movie":{"release_date":"10.21.1965"}}'

Returns: 
```json
{
    "success": true
}
```
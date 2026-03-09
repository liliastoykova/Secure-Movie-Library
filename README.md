# Secure Movie Library 

## Overview

Secure Movie Library is a FastAPI-based REST API that manages a catalog of movies and enriches them with rating data retrieved from an external API.

The application supports:

- Full CRUD operations for movies

- Authentication and authorization

- Role-based access control (ADMIN / USER)

- Background processing for external rating enrichment

- Direct SQL database queries without an ORM

Technologies Used

- Python

- FastAPI

- MariaDB / MySQL

- JWT Authentication

- pwdlib for password hashing

- Uvicorn

- unittest / MagicMock for testing

## Project Structure

~~~

Secure-Movie-Library
│
├── auth
│   ├── dependencies.py
│   ├── hashing.py
│   └── jwt_handler.py
│
├── data
│   ├── database.py
│   └── models.py
│
├── repositories
│   ├── movie_repository.py
│   └── user_repository.py
│
├── services
│   ├── movie_service.py
│   ├── user_service.py
│   └── auth_service.py
│
├── routers
│   ├── movie_router.py
│   └── auth_router.py
│
├── tests
│   └── test_movie_service.py
└── main.py
~~~

The architecture follows a layered structure:

~~~ 
Router → Service → Repository → Database
~~~


## Authentication & Authorization

Authentication is implemented using JWT tokens.

Users authenticate using:

~~~
POST /auth/login
~~~

After successful login the API returns a JWT token which must be sent in the request header:

~~~
Authorization: Bearer <token>
~~~
Passwords are stored using secure hashing (pwdlib).

## Roles

Two roles are supported:

| Role | Permissions       |
|------|-------------------|
| USER | Read-only access  |
|ADMIN | Full CRUD access  |

Authorization rules:

| Endpoint            | USER | ADMIN |
|---------------------|------|-------|
| GET /movies         | ✅    | ✅     |   
| GET /movies/{id}    | ✅    | ✅     |
| POST /movies        | ❌    | ✅     |
| PUT /movies/{id}    | ❌    | ✅     |
| DELETE /movies/{id} | ❌    | ✅     |


## Movie API Endpoints 
# Create Movie 
~~~
POST /movies
~~~
Creates a new movie.

Required fields:
~~~
title
~~~
Optional fields:
~~~
director
release_year
~~~
# Get All Movies
~~~
GET /movies
~~~
Supports:
~~~
search by title
sort by rating
~~~
Example:
~~~
GET /movies?search=up
~~~

# Get Movie by ID
~~~
GET /movies/{movie_id}
~~~
Returns a single movie.

# Update Movie
~~~
PUT /movies/{movie_id}
~~~
Updates movie details.

# Delete Movie
~~~
DELETE /movies/{movie_id}
~~~
Deletes a movie.

## External Rating Enrichment

After a movie is created, the application retrieves rating information from an external movie API.

The process runs asynchronously in the background:
~~~
Client POST /movies
        ↓
Movie saved in database
        ↓
Background task starts
        ↓
External API request (OMDb)
        ↓
Rating extracted
        ↓
Database updated
~~~
This ensures that the movie creation request returns immediately without waiting for the external API response.

## Running the Application

Install dependencies:
~~~
pip install -r requirements.txt
~~~
Run the server:
~~~
uvicorn main:app --reload
~~~
The API will be available at:
~~~
http://localhost:8000
~~~
Interactive documentation:
~~~
http://localhost:8000/docs
~~~

## Testing

Unit tests are implemented using unittest and MagicMock.

Repositories are mocked so tests do not interact with the database.

Example command:
~~~
python -m unittest
~~~

## Design Decisions

Key architectural decisions:

- Repository pattern to isolate database logic

- Service layer for business rules

- Dependency injection using FastAPI Depends

- JWT-based authentication

- Background tasks for non-blocking external API calls

- Direct SQL queries to satisfy the assignment requirement of no ORM usage
# Capstone Project

## Introduction

This project is made to satisfy the requirements for the Capstone Project in Udacity's Full Stack Nanodegree Degree. A backend API is created in Python to accept CRUD requests from authorised users. An authorisation system - RBAC (role-based access control) is set up using Auth0 to allow permitted accounts to view and perform operations on actor and movie data.

## Preparation and setup

* You will need to have Python installed - download the latest version [here](https://www.python.org/downloads/)
* Postgres is used as the database system for this project - download it [here](https://www.postgresql.org/download/)
* Extract/clone this repository to a new folder
* Open a command prompt in the root folder (the one containing ``app.py``). Run the following commands to set up the Python virtual environment:
  * Create a virtual environment with:  
    ``python3 -m venv env``  
    or if that gives an error,  
    ``python -m venv env``  
  * Then activate the virtual environment:  
    on Windows: ``env\Scripts\activate``  
    on Mac/Linux: ``source tutorial-env/bin/activate``
  * Use pip to install the required dependencies:
    ``pip3 install -r requirements.txt``

## Backend endpoint testing

Some preparation is needed for the backend and its tests to run properly, including setting up databases and environment variables. This first set of instructions will be for running the internal tests for the endpoints.
* For windows systems a batch file is provided, but will need to be edited to suit your PostgreSQL username and password.  
Edit the file ``tests.bat``, replacing "postgres" with the postgres username as instructed, and "a" with your postgres user password. Then the batch file can be run from a command prompt.
* For systems that will not run a Windows batch file, the commands will need to be input manually.
Select your preferred postgres account (username and password) and preferred database name and use the following commands:  
  * Export an environment variable so that the backend knows what path to use to access the database  
  ``export DATABASE_URL=postgresql://<YOUR_POSTGRES_USERNAME>:<YOUR_POSTGRES_PASSWORD>@localhost:5432/<DATABASE_NAME>``
  * If you have previously created a database under the database name (for example, if you have already used these instructions) drop the database -  you may be prompted to give your password:  
  ``dropdb -U <YOUR_POSTGRES_USERNAME> <DATABASE_NAME>``
  * Create a new database - you may again be prompted to give your password:  
  ``createdb -U <YOUR_POSTGRES_USERNAME> <DATABASE_NAME>``
  * Fill the database with the data needed for testing:  
  ``psql -U postgres --set ON_ERROR_STOP=on --quiet -o NUL -d capstone_test_db < test_db.sql``
  * Temporarily turn off RBAC checks using the environment variable:
    (**Note, this setting should only be used for testing purposes, do not use it in any production environment**)
  ``export CAPSTONE_RBAC_SKIP=1``
  * Run the tests - there should be 21 tests in total:
  ``python tests.py``
  * Make sure to turn on the RBAC checks after the tests are complete:
  ``export CAPSTONE_RBAC_SKIP=0``

## Setting up local server for RBAC testing

These following instructions are for setting up the backend server for external tests such as the Postman RBAC (role-based access control) test retailed below:
  * For windows systems a batch file is provided, but will need to be edited to suit your PostgreSQL username and password.  
  Edit the file ``tests.bat``, replacing "postgres" with the postgres username as instructed, and "a" with your postgres user password. Then the batch file can be run from a command prompt.
  * For systems that will not run a Windows batch file, the commands will need to be input manually. (Windows systems may also use the following if preferred, replacing ``export`` commands with ``set``)
  Select your preferred postgres account (username and password) and preferred database name and use the following commands:  
    * Export an environment variable so that the backend knows what path to use to access the database  
    ``export DATABASE_URL=postgresql://<YOUR_POSTGRES_USERNAME>:<YOUR_POSTGRES_PASSWORD>@localhost:5432/<DATABASE_NAME>``
    * If you have previously created a database under the database name (for example, if you have already used these instructions) drop the database -  you may be prompted to give your password:  
    ``dropdb -U <YOUR_POSTGRES_USERNAME> <DATABASE_NAME>``
    * Create a new database - you may again be prompted to give your password:  
    ``createdb -U <YOUR_POSTGRES_USERNAME> <DATABASE_NAME>``
    * Fill the database with the data needed for testing:  
    ``psql -U postgres --set ON_ERROR_STOP=on --quiet -o NUL -d capstone_external_db < test_db.sql``
    * Endure that RBAC checks are turned on:
    ``export CAPSTONE_RBAC_SKIP=1``
    * Setup the Flask server:
    ``flask run``
    * The server will now be ready to accept the RBAC tests.

## Running local and remote RBAC tests

* To run the RBAC (role-based access control) tests, use [Postman](https://www.postman.com).
  * To test the local server, import ``udacity-fsnd-capstone-local.postman_collection.json`` into Postman, and run the tests for the whole collection (there should be 55 tests in total). Note that this requires the external testing server to be running as described above.
  * To test the local server, import ``udacity-fsnd-capstone-remote.postman_collection.json`` into Postman, and run the tests for the ``Tests`` folder in the collection (again, there should be 55 tests in total).

## Backend models

The backend stores records for two data types: Movies and Actors. These are modelled as follows:
* Movies have data fields:
  * ``id`` (integer, internal unique id/primary key)
  * ``name`` (string) 
  * ``release_date`` (date/time record, input/output as a string)
* Actors have data fields:
  * ``id`` (integer, internal unique id/primary key)
  * ``name`` (string)
  * ``age`` (integer)
  * ``gender`` (string)

## Backend endpoints

### Overview

The API allows for sufficiently authorised users (see "Backend roles and permissions" below) to access endpoints for viewing and modifying movie and actor data.

### Error handling

When an error is encountered a response is returned with the appropriate error code and a body with some information regarding the error. Possible errors include:
* 400 - Bad request - indicates the parameters in the request body are of the incorrect type or missing entirely
* 401 - Unauthorized - indicates that the user does not have authorization for an endpoint that requires it
* 403 - Forbidden - indicates the user has some authorization, but not the correct permissions for the required endpoint
* 404 - Not found - indicates that the record being looked for is not present in the database
* 500 - Internal server error - indicates that the server has encountered an unexpected error

### Data representations

Movie and actor data are passed to and from the API using the following format:
* Movies:
  * ``id``: Unique ID (primary key) for this movie. Only for movie data returned to the caller, any ``id`` parameter given to the API will be ignored
  * ``name``: String containing the name of the movie
  * ``release_date``: String containing the release of the movie in a machine parseable form (preferably ISO, i.e. YYYY-MM-DD)
* Actors:
  * ``id``: Unique ID (primary key) for this movie. Only for actor data returned to the caller, any ``id`` parameter given to the API will be ignored
  * ``name``: String containing the actor's name
  * ``age``: Integer containing the actor's age
  * ``gender``: String describing the actor's gender

### Endpoint details

#### Movies

* ``GET /movies/<int:movie_id>``: retrieves a single movie from the database by its ID field.
  * On success, returns code 200, and a JSON body with the following parameters:
    * ``success``: ``true``
    * ``movie_data``: data representation for the requested movie
  * Possible errors: 401, 403, 404 (if no data with the given ID exists), 500
* ``POST /movies/search``: retrieves all movies whose names match a given search term
  * Must include a JSON body with parameter ``search_term``, containing a case-insensitive string to be searched for.
  * On success, returns code 200, and a JSON body with the following parameters:
    * ``success``: true
    * ``movie_data``: object containing:
      * ``count``: number of movies found matching the search string
      * ``data``: an array of movie data entries whose names match the search string
  * Possible errors: 400 (if parameter is wrong type or missing), 401, 403, 500
* ``POST /movies``: inserts a new movie into the database
  * Must include a JSON body with parameters ``name`` and ``release_date`` (see Data representations, above)
  * On success, returns code 200, and a JSON body with the following parameters:
    * ``success``: true
    * ``id``: unique id for the movie just created
  * Possible errors: 400 (if parameters are of wrong type or missing), 401, 403, 500
* ``PATCH /movies/<int:movie_id>``: updates the movie with the given id with new data
  * Must include a JSON body with parameters ``name`` and ``release_date`` (see Data representations, above)
  * On success, returns code 200, and a JSON body with the following parameter:
    * ``success``: true
  * Possible errors: 400 (if parameters are of wrong type or missing), 401, 403, 404 (if no data with the given ID exists), 500
* ``DELETE /movies/<int:movie_id>``: deletes the movie with given idea
  * On success, returns code 200, and a JSON body with the following parameter:
    * ``success``: true
  * Possible errors: 401, 403, 404 (if no data with the given ID exists), 500

#### Actors

Endpoints for actors are very similar to those the corresponding movies and for the sake of brevity will not be detailed, however, follow the endpoints for movies with the following modifications:
* Replace ``movie`` and ``movies`` with ``actor`` and ``actors`` respectively whenever the words appear
* Use the data representation for actors (``name`` as string, ``age`` as integer, ``gender`` as string) instead of the data representation when sending or receiving actor data

## Backend roles and permissions

Users may have one of three roles for accessing API endpoints. Requests that do not carry the required permissions will return a 401 or 403 errors. The three roles are:
* ``Casting Assistant``: may get and search for movie and actor data, but not modify data in any way
* ``Casting Director``: may access and modify all actor data, and view, search, and edit existing movie data. May not add or delete movies.
* ``Executive Producer``: may access all endpoints without restriction.
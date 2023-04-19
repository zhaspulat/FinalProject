import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# number to display per page
COUNT_PER_PAGE = 2 

# Enable debug mode.
DEBUG = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True
# Connect to the database


# IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = 'postgresql://<username>:<password>@localhost:5432/castagency'


AUTH0_DOMAIN = 'fsnd-instruction.us.auth0.com'
ALGORITHMS = '[RS256]'
API_AUDIENCE = 'agency_api'
AUTH0_CLIENT_ID = 'cl4MFWRvc0YAZmV5T26DmvByQKO0eLQw'
AUTH0_CLIENT_SECRET = '<secret will be provided>'

PRODUCER_TOKEN = 'Bearer <Access Token>'
ASSISTANT_TOKEN = 'Bearer <Access Token>'
import requests
import os
import json
from os.path import join, dirname
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv(verbose=True)
ENV_FILE = '.production.env' if os.environ.get(
    "PYTHON_ENV") == 'production' else '.development.env'
# dotenv_path = join(dirname(__file__), ENV_FILE)
dotenv_path = join(os.getcwd(), ENV_FILE)
# dotenv_path = '.development.env'
load_dotenv(dotenv_path)
print('---------')
print(os.getcwd())
print(dirname(__file__))

print('---------')
print('---------')

print(dotenv_path)
print(os.environ.get("TWITTER_BEARER_TOKEN"))

print('---------')
print('---------')

queries = []
query_strings = ''
if queries is not []:
    query_strings = ("?" + "".join([q + "&" for q in queries]))[:-1]
url = "https://api.twitter.com/2/tweets/search/recent{}".format(
    query_strings)

print(url)

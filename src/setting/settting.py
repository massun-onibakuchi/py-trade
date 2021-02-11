import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

TWITTER_API_KEY = os.environ.get("TWITTER_API_KEY")
TWITTER_API_SECERT = os.environ.get("TWITTER_API_SECERT")
TWITTER_BEARER_TOKEN = os.environ.get("TWITTER_BEARER_TOKEN")

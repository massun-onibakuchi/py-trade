import os
from os.path import join, dirname
from dotenv import load_dotenv

# load_dotenv(verbose=True)

# dotenv_path = join(dirname(__file__), '.env')
# load_dotenv(dotenv_path)

load_dotenv(verbose=True)
PYTHON_ENV = os.environ.get("PYTHON_ENV")
ENV_FILE = '.production.env' if PYTHON_ENV == 'production' else '.development.env'
dotenv_path = join(os.getcwd(), ENV_FILE)
load_dotenv(dotenv_path)


TWITTER_API_KEY = os.environ.get("TWITTER_API_KEY")
TWITTER_API_SECERT = os.environ.get("TWITTER_API_SECERT")
TWITTER_BEARER_TOKEN = os.environ.get("TWITTER_BEARER_TOKEN")
FTX_API_KEY = os.environ.get("FTX_API_KEY")
FTX_API_SECRET = os.environ.get("FTX_API_SECRET")
MARKET = os.environ.get("MARKET")
SUBACCOUNT = os.environ.get("SUBACCOUNT")
MAX_SIZE = os.environ.get("MAX_SIZE")

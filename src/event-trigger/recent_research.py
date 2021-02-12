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
# dotenv_path = '.development.env'
load_dotenv(dotenv_path)

print(dotenv_path)
print(os.getcwd())
print(dirname(__file__))
print(os.environ.get("TWITTER_BEARER_TOKEN"))

def auth():
    return os.environ.get("TWITTER_BEARER_TOKEN")


def create_url():
    # GET /2/tweets/search/recent
    # query = "from:elonmusk -is:retweet keyword:doge"
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    query = "from:elonmusk -is:retweet"
    tweet_fields = "tweet.fields=author_id"
    utc_date = datetime.now(timezone.utc)
    utc_date = utc_date.replace(second=(utc_date.second - 10) % 60)
    utc_date = utc_date.replace(day=(utc_date.day - 3) % 60)
    start_time_fields = "start_time=" + utc_date.strftime("%Y-%m-%dT%H:%M:%SZ")

    url = "https://api.twitter.com/2/tweets/search/recent?query={}&{}&{}".format(
        query, tweet_fields, start_time_fields)
    return url


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def connect_to_endpoint(url, headers):
    response = requests.request("GET", url, headers=headers)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def check_txt(keywords, txt):
    is_included = False
    for word in keywords:
        is_included = (word in txt) and is_included
    return is_included


def mining_txt(keywords, datas):
    is_included = False
    if datas["meta"]["result_count"] == 0:
        return is_included
    for data in datas["data"]:
        is_included = check_txt(keywords, data["text"]) or is_included
    return is_included


def main():
    bearer_token = auth()
    url = create_url()
    headers = create_headers(bearer_token)
    json_response = connect_to_endpoint(url, headers)
    res = json.dumps(json_response, indent=4, sort_keys=True)
    print("Result: \n", res)
    json_dict = json.loads(res)
    keywords = ['doge']
    mining_txt(keywords, json_dict)


if __name__ == "__main__":
    main()

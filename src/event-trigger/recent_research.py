import requests
import os
import json
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# GET /2/tweets/search/recent


def auth():
    return os.environ.get("TWITTER_BEARER_TOKEN")


def create_url():
    query = "from:elonmusk -is:retweet"
    # query = "from:elonmusk -is:retweet keyword:doge"
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    tweet_fields = "tweet.fields=author_id"
    start_time_fields = ""  # start_time
    url = "https://api.twitter.com/2/tweets/search/recent?query={}&{}".format(
        query, tweet_fields
    )
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


def check_txt(keyword, txt):
    pass

def mining_txt(keywords, datas):
    for data in datas:
        check_txt(keywords, data["txt"])


def main():
    bearer_token = auth()
    url = create_url()
    headers = create_headers(bearer_token)
    json_response = connect_to_endpoint(url, headers)
    res = json.dumps(json_response, indent=4, sort_keys=True)
    print("Result: \n", res)
    json_dict = json.loads(res)

    keywords = ['doge','']
    mining_txt(keywords,json_dict)


if __name__ == "__main__":
    main()
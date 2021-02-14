import requests
from setting.settting import LINE_BEARER_TOKEN, LINE_USER_ID
import json


def create_headers(bearer_token):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(bearer_token)
    }
    return headers


def push_message(text):
    headers = create_headers(LINE_BEARER_TOKEN)
    pay_load = {
        'to': LINE_USER_ID,
        'messages': [{
            "type": "text",
            "text": text
        }]
    }
    response = requests.request(
        "POST",
        # "https://api.line.me/v2/bot/message/push",
        "https://api.line.me/v2/bot/message/broadcast",
        headers=headers,
        data=json.dumps(pay_load))
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


if __name__ == "__main__":
    push_message("TEST_PUSH_MESSAGE")

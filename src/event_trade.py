import asyncio
from datetime import datetime, timezone
from ftx.ftx import FTX
from twitter_search.recent_research import recent_research
from setting.settting import FTX_API_KEY, FTX_API_SECRET, PYTHON_ENV, MARKET, SUBACCOUNT, MAX_SIZE
import json


class Bot:
    # ---------------------------------------- #
    # init
    # ---------------------------------------- #
    def __init__(self, api_key, api_secret):
        self.ftx = FTX(
            MARKET,
            api_key=api_key,
            api_secret=api_secret,
            subaccount=SUBACCOUNT)

        print("ENV: ", PYTHON_ENV)
        print("MARKET: ", MARKET)
        print("SUBACCOUNT: ", SUBACCOUNT)
        # タスクの設定およびイベントループの開始
        loop = asyncio.get_event_loop()
        tasks = [self.run()]

        loop.run_until_complete(asyncio.wait(tasks))

    # ---------------------------------------- #
    # bot main
    # ---------------------------------------- #
    async def run(self):
        while True:
            await self.main(5)
            await asyncio.sleep(0)

    def create_time_fields(self, sec=10):
        utc_date = datetime.now(timezone.utc)
        utc_date = utc_date.replace(second=(utc_date.second - sec) % 60)
        if PYTHON_ENV != 'production':
            utc_date = utc_date.replace(day=(utc_date.day - 3) % 60)
        start_time_fields = "start_time=" + \
            utc_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        return start_time_fields

    async def main(self, interval):
        # main処理

        """
        # account情報を取得
        self.ftx.account()
        response = await self.ftx.send()
        print(response[0])
        """

        self.ftx.positions()
        response = await self.ftx.send()
        # print(json.dumps(response[0], indent=2, sort_keys=False))
        position = ''
        for pos in response[0]["result"]:
            if pos["future"] == MARKET:
                position = pos
        print("position :>>", position)

        await asyncio.sleep(5)

        if position["size"] > float(MAX_SIZE):
            return

        query = "query=from:elonmusk -is:retweet"
        tweet_fields = "tweet.fields=author_id"
        start_time_fields = self.create_time_fields(sec=10)
        queries = [query, tweet_fields, start_time_fields]
        keywords = ['doge', 'Doge', 'DOGE']
        result = recent_research(keywords, queries)

        if len(result) > 0:
            if PYTHON_ENV == 'production':
                self.ftx.place_order(
                    type='market',
                    side='buy',
                    price='',
                    size=180,
                    postOnly=False)
            else:
                self.ftx.place_order(
                    type='limit',
                    side='buy',
                    price=1111,
                    size=0.001,
                    postOnly=True)
            response = await self.ftx.send()
            print(response[0])
            orderId = response[0]['result']['id']

        await asyncio.sleep(interval)


if __name__ == "__main__":

    Bot(api_key=FTX_API_KEY, api_secret=FTX_API_SECRET)

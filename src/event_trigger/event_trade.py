import asyncio
from ftx.ftx import FTX
from event_trigger import recent_research

class Bot:

    # ---------------------------------------- #
    # init
    # ---------------------------------------- #
    def __init__(self, api_key, api_secret):
        self.ftx = FTX(api_key=api_key, api_secret=api_secret)

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

    async def main(self, interval):
        # main処理

        """
        # account情報を取得
        self.ftx.account()
        response = await self.ftx.send()
        print(response[0])
        """

        """
       # 買い指値を注文とキャンセル
       # 注文
       self.ftx.place_order(
    type='limit',
    side='buy',
    price=10000,
    size=0.001,
     postOnly=True)
       response = await self.ftx.send()
       print(response[0])
       orderId = response[0]['result']['id']

       await asyncio.sleep(5)

       # 注文キャンセル
       self.ftx.cancel_order(orderId)
       response = await self.ftx.send()
       print(response[0])
       """

        await asyncio.sleep(interval)


if __name__ == "__main__":

    api_key = ""
    api_secret = ""

    Bot(api_key=api_key, api_secret=api_secret)

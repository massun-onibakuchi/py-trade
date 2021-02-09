import asyncio
from ftx import FTX


class Sample:

    # ---------------------------------------- #
    # init
    # ---------------------------------------- #
    def __init__(self, api_key, api_secret):
        self.ftx = FTX(api_key=api_key, api_secret=api_secret)

        # タスクの設定およびイベントループの開始
        loop = asyncio.get_event_loop()
        tasks = [self.ftx.ws_run(self.realtime), self.run()]

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
       self.ftx.place_order(type='limit', side='buy', price=10000, size=0.001, postOnly=True)
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

    # リアルタイムデータの受信
    async def realtime(self, response):
        # ここにWebSocketから配信されるデータが落ちてきますので適宜加工して利用してみてください。
        board_temp = []
        board = {'asks': {}, 'bids': {}}
        if response["channel"] == "ticker":
            print("ticer:", response)
            # 変数(板情報)
        if response['channel'] == 'orderbook':
            data = response['data']

            if data['action'] == 'partial':
                self.board_temp = data
                self.board = self.reformat_board(data)

            elif data['action'] == 'update':
                if len(self.board) > 0:
                    self.board = self.update_board(data, self.board)

            print(self.board)

    # ---------------------------------------- #
    # データ整形関数
    # ---------------------------------------- #
    # ストリーミングデータを板情報更新用の辞書データへ整形

    def reformat_board(self, data):
        board = {'asks': {}, 'bids': {}}
        for key in data.keys():
            if key == 'bids':
                board[key] = {float(quote[0]): float(quote[1])
                              for quote in data[key]}

            elif key == 'asks':
                board[key] = {float(quote[0]): float(quote[1])
                              for quote in data[key]}

        return board

    # 板情報を更新
    def update_board(self, data, board):
        for key in data.keys():
            if key in ['bids', 'asks']:
                for quote in data[key]:
                    price = float(quote[0])
                    size = float(quote[1])
                    if price in board[key]:
                        if size == 0.0:
                            # delete
                            del board[key][price]
                        else:
                            # update
                            board[key][price] = size
                    else:
                        if size > 0.0:
                            # insert
                            board[key].update({price: size})

                # sort
                if key == 'asks':
                    board[key] = {
                        key: value for key, value in sorted(
                            board[key].items())}
                elif key == 'bids':
                    board[key] = {
                        key: value for key,
                        value in sorted(
                            board[key].items(),
                            key=lambda x: -x[0])}

        return board


# --------------------------------------- #
# main
# --------------------------------------- #
if __name__ == "__main__":

    api_key = ""
    api_secret = ""

    Sample(api_key=api_key, api_secret=api_secret)

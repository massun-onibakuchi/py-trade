from datetime import datetime
import backtrader as bt
# import pyfolio as pf
from time import time


def format_time(t):
    m_, s = divmod(t, 60)
    h, m = divmod(m_, 60)
    return "Fail"
    # return f'{h:>02.0f}:{m:>02.0f}:{s:>02.0f}'


class SmaCross(bt.SignalStrategy):
    def __init__(self):
        sma1, sma2 = bt.ind.SMA(period=10), bt.ind.SMA(period=30)
        crossover = bt.ind.CrossOver(sma1, sma2)
        self.signal_add(bt.SIGNAL_LONG, crossover)


cerebro = bt.Cerebro()
cash = 10000
# comminfo = FixedCommisionScheme()
# cerebro.broker.addcommissioninfo(comminfo)
cerebro.broker.setcash(cash)

data0 = bt.feeds.YahooFinanceData(
    dataname='MSFT', fromdate=datetime(
        2011, 1, 1), todate=datetime(
            2012, 12, 31))

cerebro.adddata(data0)
cerebro.addstrategy(SmaCross)
# cerebro.addanalyzer(bt.analyzers.PyFolio, _name='pyfolio')

start = time()
results = cerebro.run()
ending_value = cerebro.broker.getvalue()
duration = time() - start

# print(f'Final Portfolio Value: {ending_value:,.2f}')
# print(f'Duration: {format_time(duration)}')
cerebro.run()
# cerebro.plot() # ERROR

import numpy as np
from get_data import read_csv_as_df

# from rqalpha.api import *
from rqalpha.apis.api_base import get_position, history_bars, subscribe
from rqalpha.utils import logger
from rqalpha.apis.api_abstract import buy_close, buy_open, sell_close, sell_open
from rqalpha.const import POSITION_DIRECTION
from rqalpha import run_func


def init(context):
    # import os
    # 获取当前运行策略的文件路径
    # strategy_file_path = context.config.base.strategy_file
    # # 根据当前策略的文件路径寻找到相对路径为 "../IF1706_20161108.csv" 的 csv 文件
    # csv_path = os.path.join(
    #     os.path.dirname(strategy_file_path),
    #     "../IF1706_20161108.csv")
    # # 读取 csv 文件并生成 df
    # IF1706_df = read_csv_as_df(csv_path)
    # 传入 context 中
    context.s1 = read_csv_as_df('/Users/masudashouta/ethereum/bot/trade-tutorial-py/quant-py/src/alphalens/data/BTC_OHLCV.csv')
    context.s2 = read_csv_as_df('/Users/masudashouta/ethereum/bot/trade-tutorial-py/quant-py/src/alphalens/data/ETH_OHLCV.csv')

    # 设置全局计数器
    context.counter = 0

    # 设置滚动窗口
    context.window = 60

    # 设置对冲手数,通过研究历史数据进行价格序列回归得到该值
    context.ratio = 15

    context.up_cross_up_limit = False
    context.down_cross_down_limit = False

    # 设置入场临界值
    context.entry_score = 2

    # 初始化时订阅合约行情。订阅之后的合约行情会在handle_bar中进行更新
    subscribe([context.s1, context.s2])


# before_trading此函数会在每天交易开始前被调用，当天只会被调用一次
def before_trading(context):
    # 样例商品期货在回测区间内有夜盘交易,所以在每日开盘前将计数器清零
    context.counter = 0


# 你选择的期货数据更新将会触发此段逻辑，例如日线或分钟线更新
def handle_bar(context, bar_dict):

    # 获取当前一对合约的仓位情况。如尚未有仓位,则对应持仓量都为0
    long_pos_a = get_position(context.s1, POSITION_DIRECTION.LONG)
    short_pos_a = get_position(context.s1, POSITION_DIRECTION.SHORT)
    long_pos_b = get_position(context.s2, POSITION_DIRECTION.LONG)
    short_pos_b = get_position(context.s2, POSITION_DIRECTION.SHORT)

    context.counter += 1
    # 当累积满一定数量的bar数据时候,进行交易逻辑的判断
    if context.counter > context.window:

        # 获取当天历史分钟线价格队列
        price_array_a = history_bars(context.s1, context.window, '1m', 'close')
        price_array_b = history_bars(context.s2, context.window, '1m', 'close')

        # 计算价差序列、其标准差、均值、上限、下限
        spread_array = price_array_a - context.ratio * price_array_b
        std = np.std(spread_array)
        mean = np.mean(spread_array)
        up_limit = mean + context.entry_score * std
        down_limit = mean - context.entry_score * std

        # 获取当前bar对应合约的收盘价格并计算价差
        price_a = bar_dict[context.s1].close
        price_b = bar_dict[context.s2].close
        spread = price_a - context.ratio * price_b

        # 如果价差低于预先计算得到的下限,则为建仓信号,'买入'价差合约
        if spread <= down_limit and not context.down_cross_down_limit:
            # 可以通过logger打印日志
            logger.info(
                'spread: {}, mean: {}, down_limit: {}'.format(
                    spread, mean, down_limit))
            logger.info('创建买入价差中...')

            # 获取当前剩余的应建仓的数量
            qty_a = 1 - long_pos_a.quantity
            qty_b = context.ratio - short_pos_b.sell_quantity

            # 由于存在成交不超过下一bar成交量25%的限制,所以可能要通过多次发单成交才能够成功建仓
            if qty_a > 0:
                buy_open(context.s1, qty_a)
            if qty_b > 0:
                sell_open(context.s2, qty_b)
            if qty_a == 0 and qty_b == 0:
                # 已成功建立价差的'多仓'
                context.down_cross_down_limit = True
                logger.info('买入价差仓位创建成功!')

        # 如果价差向上回归移动平均线,则为平仓信号
        if spread >= mean and context.down_cross_down_limit:
            logger.info(
                'spread: {}, mean: {}, down_limit: {}'.format(
                    spread, mean, down_limit))
            logger.info('对买入价差仓位进行平仓操作中...')

            # 由于存在成交不超过下一bar成交量25%的限制,所以可能要通过多次发单成交才能够成功建仓
            qty_a = long_pos_a.quantity
            qty_b = short_pos_b.quantity
            if qty_a > 0:
                sell_close(context.s1, qty_a)
            if qty_b > 0:
                buy_close(context.s2, qty_b)
            if qty_a == 0 and qty_b == 0:
                context.down_cross_down_limit = False
                logger.info('买入价差仓位平仓成功!')

        # 如果价差高于预先计算得到的上限,则为建仓信号,'卖出'价差合约
        if spread >= up_limit and not context.up_cross_up_limit:
            logger.info(
                'spread: {}, mean: {}, up_limit: {}'.format(
                    spread, mean, up_limit))
            logger.info('创建卖出价差中...')
            qty_a = 1 - short_pos_a.quantity
            qty_b = context.ratio - long_pos_b.quantity
            if qty_a > 0:
                sell_open(context.s1, qty_a)
            if qty_b > 0:
                buy_open(context.s2, qty_b)
            if qty_a == 0 and qty_b == 0:
                context.up_cross_up_limit = True
                logger.info('卖出价差仓位创建成功')

        # 如果价差向下回归移动平均线,则为平仓信号
        if spread < mean and context.up_cross_up_limit:
            logger.info(
                'spread: {}, mean: {}, up_limit: {}'.format(
                    spread, mean, up_limit))
            logger.info('对卖出价差仓位进行平仓操作中...')
            qty_a = short_pos_a.quantity
            qty_b = long_pos_b.quantity
            if qty_a > 0:
                buy_close(context.s1, qty_a)
            if qty_b > 0:
                sell_close(context.s2, qty_b)
            if qty_a == 0 and qty_b == 0:
                context.up_cross_up_limit = False
                logger.info('卖出价差仓位平仓成功!')


config = {
    "base": {
        "start_date": "2016-06-01",
        "end_date": "2016-12-01",
        "benchmark": "000300.XSHG",
        "accounts": {
            "future": 100000
        }
    },
    "extra": {
        "log_level": "error",
    },
    "mod": {
        "sys_analyser": {
            "enabled": True,
            "plot": True,
            # "record": True,
            # "output_file": "./data/result.pkl",
            # "report_save_path": "./data/result",
        },
        # "sys_accounts": {
        #     "validate_future_position": True,
        # }
    }
}

# 您可以指定您要传递的参数
run_func(
    init=init,
    before_trading=before_trading,
    handle_bar=handle_bar,
    config=config)

# from rqalpha.api import *
from rqalpha import run_func
from rqalpha.utils import logger
from rqalpha.apis.api_base import update_universe
from rqalpha.apis.api_abstract import order_percent


def init(context):
    logger.info("init")
    context.s1 = "000001.XSHE"
    update_universe(context.s1)
    context.fired = False


def before_trading(context):
    pass


def handle_bar(context, bar_dict):
    if not context.fired:
        # order_percent并且传入1代表买入该股票并且使其占有投资组合的100%
        order_percent(context.s1, 1)
        context.fired = True


config = {
    "base": {
        "start_date": "2016-06-01",
        "end_date": "2016-12-01",
        "benchmark": "000300.XSHG",
        "accounts": {
            "stock": 100000
        }
    },
    "extra": {
        "log_level": "error",
    },
    "mod": {
        "sys_analyser": {
            "enabled": True,
            "plot": True,
            "record": True,
            "output_file": "./data/result.pkl",
            "report_save_path": "./data/result",

        }
    }
}

# 您可以指定您要传递的参数
run_func(
    init=init,
    before_trading=before_trading,
    handle_bar=handle_bar,
    config=config)

# 如果你的函数命名是按照 API 规范来，则可以直接按照以下方式来运行
# run_func(**globals())

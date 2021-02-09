# run_file_demo
from rqalpha import run_file

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
        "log_level": "verbose",
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

strategy_file_path = "./pair-trad-test.py"

run_file(strategy_file_path, config)

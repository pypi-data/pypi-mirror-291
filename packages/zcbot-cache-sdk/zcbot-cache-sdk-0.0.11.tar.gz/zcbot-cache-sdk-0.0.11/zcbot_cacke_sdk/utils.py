import time
from functools import wraps


def singleton(cls):
    _instance = {}

    @wraps(cls)
    def _singlenton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singlenton


def current_timestamp10():
    """
    10位当前时间时间戳（秒级时间戳）
    :return:
    """
    return int(time.time())

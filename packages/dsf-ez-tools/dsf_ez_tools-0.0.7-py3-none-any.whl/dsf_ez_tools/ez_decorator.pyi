import time
from functools import wraps
from random import random


class MyDecorator:
    """类装饰器"""

    def __init__(self, retry_times=3): ...

    def __call__(self, func): ...


def calculate_time(func):
    """计算函数执行时间"""

import logging
import os
from logging import handlers
from logstash_async.handler import AsynchronousLogstashHandler


class Logger(object):
    """log 日志"""

    level_relations = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "crit": logging.CRITICAL,
    }

    def __init__(
        self,
        path: str = "./log",
        filename: str = "log.log",
        level: str = "info",
        when: str = "MIDNIGHT",
        interval: int = 1,
        backup_count: int = 3,
        max_bytes: int = None,
        fmt: str = "%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s",
        is_save_file: bool = True,
        is_push_logstash: bool = False,
        is_print: bool = True,
        logstash_host: str = None,
        logstash_port: int = None,
    ):
        """@param path: 日志文件存储路径
        @param filename: 日志文件名
        @param level: 日志等级
        @param when: 日志文件按什么维度切分。'S'-秒；'M'-分钟；'H'-小时；'D'-天；'W'-周
                这里需要注意，如果选择 D-天，那么这个不是严格意义上的'天'，而是从你
                项目启动开始，过了24小时，才会从新创建一个新的日志文件，
                如果项目重启，这个时间就会重置。所以这里选择'MIDNIGHT'-是指过了午夜12点，就会创建新的日志。
        @param interval：是指等待多少个单位 when 的时间后，Logger会自动重建文件。
        @param backup_count: 日志文件保留的个数，为0是时会自动删除掉日志。

        @param max_bytes:
        @param fmt: 日志格式
        @param is_save_file: 是否将日志保存到文件
        @param is_push_logstash: 是否将日志推入 logstash
        @param is_print: 是否在控制台打印日志"""

import logging
import pymysql
from dbutils.pooled_db import PooledDB
from pymysql.constants import CLIENT


class MysqlPoolClientWrapper:

    def __init__(self, config: dict): ...

    @property
    def pool(self):
        """缓存初始化mq客户端"""

    def connect(self):
        """启动连接
        :return:"""

    def connect_close(self, conn, cursor):
        """关闭连接
        :param conn:
        :param cursor:
        :return:"""

    def fetch_all(self, sql):
        """批量查询
        :param sql:
        :param args:
        :return:"""

    def fetch_one(self, sql, args):
        """查询单条数据
        :param sql:
        :param args:
        :return:"""

    def insert(self, sql):
        """插入数据
        :param sql:
        :param args:
        :return:"""

    def insert_lot(self, sql, result_list):
        """插入数据
        :param sql:
        :param args:
        :return:"""

    def execute_batch_queries(self, sql_statements, batch_size=200): ...

    def execute_multi_query(self, sql_statements): ...

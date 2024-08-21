import logging
import time
import traceback
from functools import wraps
import pymysql.cursors
from loguru import logger


def measure_time(func): ...


class MysqlClientWrapper(object):
    """
    包含mysql 的各种操作：自定义连接、增删查改表数据 （单个、批量）
    提供超时自动重连机制，避免长期未使用conn导致断连，从而影响sql语句的执行。
    提供以 dict 的形式拼接成常见的 sql，这样可以减少手动写sql的时间；
    """

    def __init__(self, config): ...

    def _connect(self): ...

    def reconnect(self):
        """重连，避免因太久未操作数据库而导致连接断开"""

    def _execute(self, *args, **kwargs):
        """给execute增加重连机制"""

    def create_db(self, db_name: str):
        """建库语句，建库后 use该库"""

    def create_table(self, create_table_sql: str):
        """在当前数据库中创建数据表"""

    def delete_table(self, delete_table_name: str):
        """删除数据表"""

    @measure_time
    def insert_one(self, table_name: str, data_dict: dict, mode=0) -> int:
        """增加单条数据
        @param table_name: 表名
        @param data_dict:
        @param mode: 直接新增遇错报错；新增遇错跳过忽略；新增遇重复prim key则更新；
        @return:"""

    @measure_time
    def insert_many(self, table_name: str, data_dict_ls: list, mode=0) -> int:
        """多数据插入
        "insert into data_market_symbol_info (Bourse_Id,Symbol) values (%s,%s);"  args: [(a,b),(c,d)]
        """

    @measure_time
    def update_one(self, table_name: str, data_dict: dict): ...

    @measure_time
    def update_many(self, table_name: str, data_dict_ls: list): ...

    @measure_time
    def delete_one(self, table_name: str, data_dict: dict) -> tuple:
        """:return: Tuple[Any, ...]"""

    @measure_time
    def query_one(self, query_sql: str, args=None) -> tuple:
        """:return: Tuple[Any, ...]"""

    @measure_time
    def query_many(self, query_sql: str, args=None) -> tuple:
        """:return:   Tuple[Tuple[Any, ...], ...]"""

    def execute_multi_sql(self, multi_sql: str) -> list:
        """执行多条sql语句,并获取各个sql语句的值
                @param multi_sql:  'SELECT SQL_CALC_FOUND_ROWS  target_id,id FROM tb_community_comment WHERE target_id=131;
        SELECT FOUND_ROWS();'
                @return:
        """

    def _concatenate_delete_sql(
        self, table_name: str, data_dict: dict, mode=0
    ) -> tuple:
        """拼接delete sql语句
        :param table_name: 表名
        :param data_dict: 字段名+数据字典
        DELETE FROM students WHERE id = 1 and b =2;"""

    def _concatenate_insert_sql(
        self, table_name: str, data_dict: dict, mode=0
    ) -> tuple:
        """拼接插入sql语句
        3种execute demo :
            "insert into info (Bourse_Id,Symbol) values ('51201','1234');"
            "insert info (Bourse_Id,Symbol) values (%s,%s);" args = ('51202', '5678')
            "insert into info (Bourse_Id,Symbol) values (%(b_id)s,%(symbol)s);" args = {"b_id": "51203", "symbol": "abcd"}
        :param table_name: 表名
        :param data_dict: 字段名+数据字典
        重复数据：根据主键或者唯一索引判断
        :param mode: 插入模式 0: insert into     重复数据时抛出异常
                              1: insert ignore  重复数据时忽略当前新数据
                              2: replace into    重复数据时先删除旧数据再新数据（字段不全设置为默认值），否则与insert一样
                              3: insert into ... ON DUPLICATE KEY UPDATE ...    会检查插入的数据主键是否冲突，如果冲突则执行更新操作，如果ON DUPLICATE KEY UPDATE的子句中要更新的值与原来的值都一样，则不更新。如果有一个值与原值不一样，则更新
        """

    def _concatenate_many_insert_sql(
        self, table_name: str, data_dict_ls: list, mode=0
    ) -> tuple:
        """拼接批量插入sql语句,借用_concatenate_insert_sql生成sql语法"""

    @staticmethod
    def get_args_from_insert_data(data_dict: dict):
        """从 data_dict 中拼接出 insert sql需要的args"""

    @staticmethod
    def get_args_from_update_data(data_dict: dict):
        """从 data_dict 中拼接出 update sql需要的args"""

    def _concatenate_update_sql(self, table_name: str, data_dict: dict) -> tuple:
        """拼接update sql语句
        " update data_market_symbol_info set a=1, b='x', c=NULL where a=1 and b='x' and c=NULL;"
        :param table_name :"data_market_symbol_info"
        :param {
            "set":{"a":1,"b":"x","c":None},
            "where":{"a":1,"b":"x","c":None}
        }"""

    def _concatenate_many_update_sql(
        self, table_name: str, data_dict_ls: list
    ) -> tuple:
        """拼接批量更新sql语句,借用 _concatenate_update_sql 生成sql语法"""

    def close(self): ...

    def __del__(self): ...


class Connection(object):
    """A lightweight wrapper around PyMySQL."""

    def __init__(
        self,
        host,
        database,
        user=None,
        password=None,
        port=0,
        max_idle_time=7 * 3600,
        connect_timeout=10,
        time_zone="+0:00",
        charset="utf8mb4",
        sql_mode="TRADITIONAL",
    ): ...

    def _ensure_connected(self): ...

    def _cursor(self): ...

    def __del__(self): ...

    def close(self):
        """Closes this database connection."""

    def reconnect(self):
        """Closes the existing database connection and re-opens it."""

    def query(self, query, *parameters, **kwparameters):
        """Returns a row list for the given query and parameters."""

    def get(self, query, *parameters, **kwparameters):
        """Returns the (singular) row returned by the given query."""

    def execute(self, query, *parameters, **kwparameters):
        """Executes the given query, returning the lastrowid from the query."""

    def execute_params(self, query, params):
        """Executes the given query, returning the lastrowid from the query."""

    insert = execute

    def table_has(self, table_name, field, value): ...

    def table_insert(self, table_name, item):
        """item is a dict : key is mysql table field"""

    def table_update(self, table_name, updates, field_where, value_where):
        """updates is a dict of {field_update:value_update}"""

    def execute_(self, query, params=None):
        """Executes the given query, returning the lastrowid from the query."""

    def execute_many_params(self, query, params):
        """Executes the given query, returning the lastrowid from the query."""

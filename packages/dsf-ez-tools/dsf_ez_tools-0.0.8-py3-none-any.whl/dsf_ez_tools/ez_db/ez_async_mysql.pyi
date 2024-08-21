import asyncio
import logging
import time
from typing import Optional
from aiomysql import Pool, create_pool
from aiomysql.cursors import DictCursor


class AsyncMysqlConnection:
    """
    异步mysql链接
    """

    def __init__(
        self,
        host,
        database,
        user=None,
        password=None,
        port=3306,
        connect_timeout=10,
        charset="utf8mb4",
        sql_mode="TRADITIONAL",
        time_zone="+00:00",
        autocommit=False,
        loop: Optional[asyncio.AbstractEventLoop] = None,
        *args,
        **kwargs
    ): ...

    def __del__(self): ...

    async def reconnect(self):
        """建立链接池"""

    async def close(self):
        """关闭连接池"""

    async def _cursor(self):
        """返回游标"""

    async def query(self, query, *args, **kw):
        """查询全部"""

    async def query_yield(self, query, page_number=None, page_size=None, *args, **kw):
        """异步迭代查询全部"""

    async def get(self, query, *args, **kw):
        """查询一条"""

    async def execute(self, sql, *args, **kw):
        """执行语句"""

    async def execute_params(self, sql, params):
        """执行参数"""

    async def execute_many_params(self, sql, params):
        """执行多参数"""

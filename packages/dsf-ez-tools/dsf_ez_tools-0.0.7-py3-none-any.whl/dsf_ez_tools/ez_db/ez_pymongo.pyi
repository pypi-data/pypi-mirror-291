import pymongo.database
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.read_preferences import ReadPreference


class Database(object):
    """
    内部数据库配置
    """

    id = "_id"
    type = "type"
    label = "label"
    host = "host"
    database = "database"
    user = "user"
    password = "password"
    replica = "replica"


class DatabaseType(object):
    """
    数据库类型
    """

    mongodb = "mongodb"


class TableMeta(object):
    """
    mongo数据表路由配置元数据，指定哪个表存在哪个数据库中
    """

    id = "_id"
    table_name = "table_name"
    database_id = "database_id"


INTER_DATABASES = [
    {
        Database.id: "mongo-4",
        Database.type: DatabaseType.mongodb,
        Database.label: "联系方式",
        Database.host: "localhost:27017",
        Database.database: "mongo-4-db",
        Database.user: None,
        Database.password: None,
        Database.replica: "",
    },
    {
        Database.id: "mongo-6",
        Database.type: DatabaseType.mongodb,
        Database.label: "企业表",
        Database.host: "localhost:27017",
        Database.database: "mongo-6-db",
        Database.user: None,
        Database.password: None,
        Database.replica: "",
    },
]
ROUTE_CONFIGS = [
    {TableMeta.table_name: "dsf", TableMeta.database_id: "mongo-6"},
    {TableMeta.table_name: "enterprise", TableMeta.database_id: "mongo-6"},
    {TableMeta.table_name: "contact", TableMeta.database_id: "mongo-4"},
]


class MongoDBClientWrapper:

    def __init__(self): ...

    def database_4_collection(self, col_name: str) -> pymongo.database.Database:
        """通过遍历数据库表路由配置 获取数据库db链接
        @param col_name: 表名
        @return: Database对象"""

    def p_col(self, col_name: str) -> Collection:
        """通过col_name获取其所在db，然后获取其 collection对象
        @param col_name: 表名
        @return:collection对象"""

    def s_col(self, col_name: str) -> Collection:
        """与 p_col 一样，只不过是从从节点获取 Collection"""

    def close(self): ...

    def __del__(self):
        """批量断开数据库连接"""

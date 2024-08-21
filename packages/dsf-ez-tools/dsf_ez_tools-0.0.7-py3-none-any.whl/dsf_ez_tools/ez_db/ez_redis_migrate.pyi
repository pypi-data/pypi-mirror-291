from loguru import logger
from ez_redis import RedisClientWrapper


class RedisMigrater:
    """
    用于将源redis的各个db中的各个key迁移到目标redis中，且不影响目标redis中的已有数据
    """

    def __init__(
        self,
        source_redis_config: dict,
        target_redis_config: dict,
        mode="a",
        migrate_db_map: {} = None,
    ):
        """:param source_redis_config: 源redis的配置
        :param target_redis_config: 目前redis的配置
        :param mode: 迁移模式，a：追加模式，如果目标db中已有该key，会将迁移数据追加进去。 w：覆盖模式，如果目标db中已有该key，则先删除key再重写
        :param migrate_db_map: 源db id 与 目标db id的映射，即将源db迁移到目标db的指定id"""

    def main(self):
        """实现方案：
        1、根据db数量进行循环，每次循环将源redis与目标redis都切换到对应的db
        2、遍历源db中的所有的key，判断key的类型
        3、根据key的类型，从源redis中取值，然后写入到目标target"""

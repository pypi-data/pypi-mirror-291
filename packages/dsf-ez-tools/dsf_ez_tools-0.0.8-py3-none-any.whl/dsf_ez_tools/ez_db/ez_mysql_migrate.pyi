import os
from loguru import logger


class MysqlMigrater:
    """
    用于将源mysql的各个db迁移到目标mysql中，会直接覆盖目标mysql db中的数据

    要注意不同服务器安装的mysql版本，不同版本支持的数据集不一样，例如源mysql使用 utf8mb4_0900_ai_ci 数据集而目标mysql不支持这个，就会
    报错 ERROR 1273 (HY000) at line 119: Unknown collation: 'utf8mb4_0900_ai_ci'，导致这个表迁移失败。

    对于大型数据库，可以使用mysqldump配合管道直接将数据从一个数据库服务器传输到另一个，减少磁盘I/O操作。
    对于小型数据库，可以读取源db的所有数据，然后写入到目标db中
    """

    def __init__(self, source_mysql_config: dict, target_mysql_config: dict):
        """:param source_mysql_config: 源mysql的配置
        :param target_mysql_config: 目标mysql的配置"""

    def pipeline_migrate(self):
        """通过 mysqldump 管道直接将源db中的数据迁移到目标db中，不会生成中间文件；
        优点：快、不会生成中间文件
        缺点：当网络不稳定时，可能导致整个任务失败，需要重头开始
        :return:"""

    def generate_sql_file_migrate(self):
        """通过 mysqldump先导出源db的数据到中间sql文件，再通过mysqldump将该sql文件的内容导入到 目标db中
        优点：生成中间sql文件后，如果导入失败只需要再次导入，而不用再次重头导出生成中间文件
        缺点：慢，会生成中间文件
        当然导入导出都可以到对应服务器进行，通过scp将中间文件在服务器间传输
        :return:"""

    def clean_cmd(self, cmd: str) -> str:
        """清洗cmd命令"""

    def main(self):
        """实现方案：
        1、mysqldump迁移，如果目标服务器不存在该db则新建，如果存在db且存在源db中的表，则会drop表再写入数据，也就是源db会覆盖目标db中的数据"""

import json
from kafka import KafkaProducer, KafkaConsumer, TopicPartition


class KafkaProducerWorker(object):
    """
    一个kafka集群有若干broker即kafka实例，每个服务器有若干broker；
    一个kafka集群内的每个broker都有一个不重复的编号。

    生产者和消费者都是面向topic，一个broker中有若干topic用于存储不同类别的消息。
    一个topic有若干partition有序队列，且各个partition的数据是不重复的。
    一个partition 有若干副本分为一个leader和其他follower，follower和leader绝对是在不同的broker，
    同一broker中对同一partition只能存放一个副本。

    生产者发送数据到leader partition中，然后follower会去leader处自行同步数据。
    消费者消费数据也是从leader partition中消费数据。

    消费者组是一个逻辑上的订阅者，有若干消费者，组内每个消费者消费不同partition，一个partition只能被一个消费者消费，
    一个消费者可以消费多个partition。消费者之间互不影响。

    已有的消费者想重头消费信息，可以修改偏移量 ：KafkaConsumer.seek(0)
    或者新增消费者组，这将使 Kafka 认为您正在使用一个新的消费者组，并从起始偏移量开始重新消费消息



    控制一条消息从客户端生产者，到kafka分区存储，再到消费者消费的完整流程

    """

    def __init__(self, bootstrap_servers): ...

    def create_producer(self):
        """bootstrap_servers (str or list):  Kafka 集群的地址列表，格式为 host[:port]，例如 ['localhost:9092']
        key_serializer: 用于将消息的键序列化为字节的函数
        value_serializer: 用于将消息的值序列化为字节的函数
        :return:"""

    def send_data(self, topic, data, partition=None): ...

    @staticmethod
    def on_send_success(record_metadata): ...

    @staticmethod
    def on_send_error(error_info): ...


class KafkaConsumerWorker(object):

    def __init__(
        self,
        bootstrap_servers: str or list,
        group_id: str,
        topic: str = None,
        auto_offset_reset="latest",
        enable_auto_commit=True,
    ):
        """@param bootstrap_servers: (str or list)  Kafka 集群的地址列表，格式为 host[:port]，例如 ['localhost:9092']
        @param group_id:  指定消费者组id,也可以不指定
        @param topic: topic名称
        @param auto_offset_reset: 消费者从哪开始消费 latest：从最新消费   earliest：从最老消息开始消费
        @param enable_auto_commit: 消费完该数据后是否自动commit，若为False，则需要手动commit，consumer.commit()
        """

    def create_consumer(self): ...

    def receive_data_from_partition(self, topic: str, partition: str):
        """指定 topic的分区进行消费
        如果enable_auto_commit为False，则接收之后需要 consumer.commit()
        @param topic: 主题名
        @param partition: 分区名
        @return:"""

    def receive_data_from_topics(self, topics: list):
        """订阅多个topic,可同时接收多个topic消息进行消费
        @param topics: 主题列表 ["CRStockTick1","CRStockTick22"]"""

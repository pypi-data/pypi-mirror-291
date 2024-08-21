import threading
import time
import traceback
import typing
from datetime import datetime
import zmq
from loguru import logger


class ZmqPublisher:

    def __init__(self, zmq_url: str = "tcp://*:7020"): ...

    def zmq_heartbeat(self, socket, msg):
        """zmq的心跳线程执行的函数
        :param socket:
        :param msg:
        :return:"""

    def run_heartbeat_thread(self, zmq_socket, heartbeat_content: str = "HeartBeat"):
        """运行心跳线程
        :param zmq_socket:
        :param heartbeat_content:
        :return:"""

    @property
    def publisher(self) -> zmq.Socket:
        """缓存获取发布者socket
        @return:"""

    def _get_publisher_socket(self, mode: int = 1) -> zmq.Socket:
        """获取发布者socket
        :param mode: 1:普通发布者 2：broker模式的发布者"""

    def send(self, data: bytes, retry_times: int = 3) -> bool:
        """对外暴露发布数据的方法，客户端只需调用该方法发送数据即可，方法内部会连接zmq、错误重试
        :param data: 要发布的数据
        :return: 返回是否发送成功"""

    def as_server(self, generate: typing.Iterable, mode: int = 1) -> None:
        """发布者，一直发布消息；
        应用场景：
        1、在程序有源源不断的tick时，嵌入程序将这些tick发出去
        2、从一个固定的数据源中不断取出tick进行发生，这是分离式的
        :param mode: 1:普通发布者 2：broker模式的发布者"""


class ZmqSubscriber:

    def __init__(self, zmq_url: str = "tcp://localhost:7020"): ...

    @property
    def subscriber(self) -> zmq.Socket:
        """缓存获取订阅者socket"""

    def _get_subscriber_socket(self, topic: str = "") -> zmq.Socket:
        """获取订阅者socket
        @param topic: 话题"""

    def recv(self, retry_times: int = 3) -> typing.ByteString:
        """对外暴露获取数据的方法，客户端只需调用该方法即可接收原始数据，方法内部会连接zmq、错误重试
        @return: 原始bytes类型的字符串"""


def zmq_sub_thread(): ...


def zmq_pub_thread(): ...

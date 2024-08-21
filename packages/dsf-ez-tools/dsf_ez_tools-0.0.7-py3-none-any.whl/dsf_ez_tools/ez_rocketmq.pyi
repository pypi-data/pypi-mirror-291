import datetime
import json
import logging
import random
import typing
from mq_http_sdk.mq_client import MQClient
from mq_http_sdk.mq_producer import TopicMessage, MQExceptionBase

try:
    from rocketmq.client import Producer, Message
except NotImplementedError as NIE:
    print(f"\x1b[1;31m 请不要在 window 上调试 {NIE} \x1b[0m")


class AlRocketMQ:

    def __init__(
        self,
        host: str,
        access_id: str,
        access_key: str,
        instance_id: str,
        topic_name: str,
        logger=None,
    ):
        """@param host: 设置HTTP接入域名
        @param access_id: AccessKey 阿里云身份验证，在阿里云服务器管理控制台创建
        @param access_key: SecretKey 阿里云身份验证，在阿里云服务器管理控制台创建
        @param instance_id:
        @param topic_name:
        @param logger:"""

    def shut_down(self): ...

    @property
    def mq_client(self):
        """缓存初始化mq客户端"""

    @property
    def mq_producer(self):
        """缓存初始化生产者"""

    def _send_rocket_mq_message(self, message_body: str, message_tag, text="") -> bool:
        """:param message_body: 消息体
        :param message_tag: 消息标签
        :return 是否发送成功"""

    def send_message(
        self,
        message: typing.Union[typing.List, typing.Dict, typing.AnyStr],
        tag="",
        text="",
    ) -> bool: ...


class RocketMQProducer:

    def __init__(self, host: str, topic_name: str, pid_name: str, logger=None):
        """@param host: 设置HTTP接入域名
        @param topic_name:
        @param pid_name:
        @param logger:"""

    def shut_down(self): ...

    @property
    def mq_producer(self):
        """缓存初始化生产者"""

    def send_message(
        self,
        message: typing.Union[typing.List, typing.Dict, typing.AnyStr],
        tag: str = "",
        text: str = "",
        use_async=False,
    ) -> bool:
        """发送消息给mq
        @param message: 消息体
        @param tag:
        @param text:
        @param use_async: 是否异步发送
        @return:"""

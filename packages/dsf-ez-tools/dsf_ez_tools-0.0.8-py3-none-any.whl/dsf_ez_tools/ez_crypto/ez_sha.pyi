import hashlib
import hmac
import typing
from base import BaseEncryptHelper


class ShaHelper(BaseEncryptHelper):
    """
    sha系列加密工具
    """

    def __init__(self, algorithm="sha1"):
        """:param algorithm: 使用的加密算法， sha1、sha224等"""

    def encrypt(self, origin_data: typing.Union[str, bytes]) -> bytes:
        """使用指定的 sha算法将原始数据进行sha加密
        :param origin_data: 原始数据
        :param algorithm: 指定sha算法
        :return:"""


class HmacShaHelper(BaseEncryptHelper):
    """
    Hmacsha 系列加密工具
    """

    def __init__(self, hmac_key: typing.Union[bytes, str] = "", algorithm="sha1"):
        """:param hmac_key: 加盐
        :param algorithm: 使用的加密算法， sha1、sha224等"""

    def encrypt(self, origin_data: typing.Union[str, bytes]) -> bytes:
        """使用指定的 sha算法将原始数据进行sha加密
        :param origin_data: 原始数据
        :param algorithm: 指定sha算法
        :return:"""

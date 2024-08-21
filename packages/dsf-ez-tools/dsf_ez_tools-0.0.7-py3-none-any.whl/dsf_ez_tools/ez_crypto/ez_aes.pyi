import json
import typing
from Crypto.Cipher import AES
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import algorithms
from loguru import logger
from base import BaseDecryptHelper


class AESHelper(BaseDecryptHelper):

    def __init__(
        self,
        key: typing.Union[str, bytes],
        iv: typing.Union[str, bytes] = "",
        mode: str = "ECB",
    ):
        """@param key: 密钥  必须 16, 24 or 32 bytes long 分别对应 *AES-128*,*AES-192* or *AES-256*
        @param iv:  密钥偏移量 CBC模式中必须提供长16字节;ECB模式不用IV
        @param mode: 加密模式: ECB、CBC"""

    @property
    def cryptor(self): ...

    def encrypt(self, data: typing.Union[str, bytes]) -> bytes:
        """AES加密
        @param text: Bytes to be encrypted
        @return:"""

    @staticmethod
    def pkcs7_padding(data: typing.Union[str, bytes]) -> bytes:
        """使用pkcs7_padding 填充模式对原始数据进行填充

        PKCS#7填充模式的基本思路是在原数据的末尾添加若干字节，这些字节的值等于所需填充的字节数。
        例如，如果原数据的长度是 10 字节，那么需要添加 6 字节的填充，每个字节的值为 0x06。解密后，需要移除这些填充字节以还原原始数据。

        @param data: 原始数据
        @return: 填充后的数据"""

    @staticmethod
    def pkcs7_unpadding(padded_data: bytes) -> bytes:
        """反填充，从填充后的数据中还原出原始数据
        :param padded_data: 填充后的数据
        :return:"""

    def decrypt(self, data: bytes) -> bytes: ...

    def dict_json(self, d):
        """python字典转json字符串, 去掉一些空格"""

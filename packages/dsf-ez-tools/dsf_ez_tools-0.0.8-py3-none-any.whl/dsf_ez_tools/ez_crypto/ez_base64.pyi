import typing
from base64 import b64decode
from base64 import b64encode


class Base64Helper:
    """
    Base64 加解密
    """

    @staticmethod
    def encrypt(clear_string: str) -> str:
        """使用Base64将明文字符串编码并返回编码后的密文字符串
        :param clear_string: 明文字符串
        :return: 加密后的密文字符串"""

    @staticmethod
    def decrypt(cipher_string: typing.Union[str, bytes]) -> bytes:
        """Base64 解码 bytes-like object or ASCII string 为明文字节流，
        注意图片明文字节流不能直接decode为字符串，因此返回字节流
        :param cipher_string: 密文字符串或bytes
        :return: 明文字节流"""

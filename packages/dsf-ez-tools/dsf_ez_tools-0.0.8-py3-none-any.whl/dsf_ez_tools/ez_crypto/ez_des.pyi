import typing
from pyDes import des, CBC, PAD_PKCS5, PAD_NORMAL, ECB, triple_des
from base import BaseDecryptHelper


class DESHelper(BaseDecryptHelper):

    def __init__(
        self,
        key: typing.Union[str, bytes],
        iv: typing.Union[str, bytes] = "",
        mode=ECB,
        pad=None,
        padmode=PAD_NORMAL,
    ):
        """@param key:  密钥，必须正好8字节
        @param iv:  密钥偏移量，CBC模式中必须提供8字节长度iv;ECB模式不用IV
        @param mode:  加密模式：ECB、CBC
        @param pad:加密填充的可选参数。必须只有一个字节
        @param padmode: 加密填充模式PAD_NORMAL(即 no padding) or PAD_PKCS5"""

    def encrypt(self, data: typing.Union[str, bytes]) -> bytes:
        """DES 加密
        :param data: Bytes to be encrypted
        :return: 加密后bytes"""

    def decrypt(self, data: typing.Union[str, bytes]) -> str:
        """DES 解密
        :param data: Bytes to be decrypted
        :return:  解密后的字节流"""


class DES3Helper(BaseDecryptHelper):

    def __init__(
        self,
        key: typing.Union[str, bytes],
        iv: typing.Union[str, bytes],
        mode=ECB,
        pad=None,
        padmode=PAD_NORMAL,
    ):
        """@param key: 密钥 必须 16 or 24 byte
        @param iv:  密钥偏移量 CBC模式必须要提供8字节长度iv，ECB模式不用IV
        @param mode:加密模式  ECB,CBC
        @param pad: 加密填充的可选参数。必须只有一个字节
        @param padmode: PAD_NORMAL or PAD_PKCS5"""

    def encrypt(self, data: typing.Union[str, bytes]) -> bytes:
        """使用指定的加密方法对原始数据进行DES3加密
        :param origin_data: 明文原始数据
        :return: 加密后的数据"""

    def decrypt(self, data: typing.Union[str, bytes]) -> str:
        """DES3 解密密文得到明文
        :param data: Bytes to be decrypted
        :return:  解密后的字节流"""

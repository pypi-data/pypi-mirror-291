import binascii
from typing import Union


class HexHelper:
    """
    binascii.b2a_hex
    b表示正常字符串，a表示hex字符串
    """

    @staticmethod
    def data_to_hex_string(data: Union[str, bytes]) -> str:
        """将明文字符串或字节流转 hex 字符串
        字符串 >> 二进制 >> hex >> hex 字符串
        :param data:
        :return:"""

    @staticmethod
    def hex_string_to_data(hex_str: str) -> bytes:
        """将 hex 字符串转明文字符串字节流
        hex 字符串 >> hex >> 二进制"""

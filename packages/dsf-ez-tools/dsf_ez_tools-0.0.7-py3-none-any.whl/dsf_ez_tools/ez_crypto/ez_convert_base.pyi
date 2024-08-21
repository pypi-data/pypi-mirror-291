import typing


class BaseConvertHelper:
    """
    进制转换工具，用于不同进制之间的互相转换
    """

    @staticmethod
    def convert_10_to_any_base(
        value: typing.Union[int, str], base: int, result_length: int
    ) -> str:
        """将10进制转换为 length位的任意进制字符串
        :param value: 十进制原值
        :param base: 要转为的指定进制
        :param result_length: 转换成指定进制字符串后的长度
        :return:"""

    @staticmethod
    def convert_any_base_to_10(value: str, value_base) -> int:
        """将任意进制的字符串转换为十进制数
        :param value: 原值
        :param value_base: 原值的进制
        :return:"""

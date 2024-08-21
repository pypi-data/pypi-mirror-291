import typing


class DataTypeConvertHelper:
    """
    数据类型转换工具，用于将不同类型的数据互相转换
    """

    @staticmethod
    def bytesToHexString(bArr: typing.Union[bytes, bytearray]) -> str:
        """:param bArr:
        :return:"""

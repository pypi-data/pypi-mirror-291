import typing
from base64 import b64encode, b64decode


class BaseEncryptHelper:
    """
    加密的基类，定义基础的加密方法
    加密成字节流、但是一般不直接传递字节流，而是传递其hex、或base64编码后的字符串
    """

    def cut_bytes_to_length(
        self, data: typing.Union[bytes, bytearray], special_length: int
    ) -> bytes:
        """裁剪字节流到指定长度
        :param special_length:
        :return:"""

    def data_to_bytes(self, data: typing.Any) -> bytes:
        """将任意类型数据转为bytes"""

    def data_to_str(self, data: typing.Any) -> str:
        """将任意类型数据转为str"""

    def encrypt(self, origin_data: typing.Union[str, bytes]) -> bytes:
        """将源数据进行加密，得到加密后的字节流
        :param origin_data:
        :return:"""

    def encryptToHexStr(self, data: typing.Union[str, bytes]) -> str:
        """先进行算法加密，得到密文字节流，再转为Hex格式"""

    def encryptToBase64Str(self, data: typing.Union[str, bytes]) -> str:
        """先进行算法加密，得到密文字节流，再转为 Base64 格式"""


class BaseDecryptHelper(BaseEncryptHelper):
    """
    加解密的基类，定义基础的解密密方法,
    解密成字节流。因为原始数据可能是图片、文件等，如果我们直接解密转为字符串，可能会报错，
    因此我们只解密为原始字节流，客户端再根据自己需求进行存储或转为字符串
    """

    def decrypt(self, data: typing.Union[str, bytes]) -> bytes:
        """将加密后的字节数据进行加密，得到解密后的字节流
        :param data: Bytes to be encrypted
        :return:  解密后的字节流"""

    def decryptFromHexStr(self, data: typing.Union[str, bytes]) -> bytes:
        """将hex字符串或字节流先hex解码为原始密文字节流，再进行算法解密
        :param data: Bytes to be encrypted
        :return:  解密后的字节流"""

    def decryptFromBase64Str(self, data: typing.Union[str, bytes]) -> bytes:
        """将base64字符串或字节流先base64解码为原始密文字节流，再进行算法解密
        :param data: Bytes to be encrypted
        :return:  解密后的字节流"""

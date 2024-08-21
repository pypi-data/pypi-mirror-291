import hashlib
import typing
from base import BaseEncryptHelper


class Md5Helper(BaseEncryptHelper):
    """
    提供快速md5，并可指定位数的功能
    """

    def encrypt(self, origin_data: typing.Union[str, bytes]) -> bytes:
        """MessageDigest md5 = MessageDigest.getInstance("MD5"); 生成一个MD5加密计算摘要
        md5.reset(); 清除默认缓存
        md5.update(targetStr.getBytes());  将字符串转换为字节数组,计算md5函数
        byte[] digest = md5.digest(); //信息摘要对象对字节数组进行摘要,得到摘要字节数组表示的hash值
        BigInteger bigInt = new BigInteger(1, digest);
        String hashText = bigInt.toString(16);   转换为16进制字符串表示的hash值
        while(hashText.length() < 32 ){
            hashText = "0" + hashText; BigInteger会把0省略掉，需补全至32位
        }
        @return 摘要字节流"""

    def to_md5(
        self,
        origin_data: typing.Union[str, bytes],
        digit: typing.Literal[16, 32, 40] = 32,
    ) -> str:
        """支持16, 32位的16进制md5
        @param origin_data: 原始数据
        @param digit: 生成的摘要位数
        @return:"""

import typing
import rsa
from Crypto.PublicKey import RSA
from base import BaseDecryptHelper


class RsaHelper(BaseDecryptHelper):
    """
    Rsa多种格式密钥，进行公钥加密、私钥解密、验签、生成不同格式的密钥文件等操作
    """

    def __init__(
        self,
        public_key: typing.Union[bytes, str] = None,
        private_key: typing.Union[bytes, str] = None,
        format_="PEM",
    ):
        """:param public_key: 公钥
        :param private_key: 私钥
        :param format: 生成key的格式，可以是PEM或DER 格式，默认PEM格式"""

    def encrypt_by_pkcs1(self, origin_data: typing.Union[str, bytes]) -> bytes:
        """RSA加密，以 -----BEGIN RSA PUBLIC KEY----- 开头的公钥使用该方法进行加密
        :param origin_data: 明文原始数据
        :return: 加密后的数据"""

    def encrypt_by_pkcs1_openssl_pem(
        self, origin_data: typing.Union[str, bytes]
    ) -> bytes:
        """RSA加密，针对setPublicKey， 以-----BEGIN PUBLIC KEY----- 开头的公钥使用该方法进行加密
        :param origin_data: 明文原始数据
        :return: 加密后的数据"""

    def encrypt_by_e_n(self, origin_data: typing.Union[str, bytes]) -> bytes:
        """RSA加密，针对new RSAKeyPair
        :param origin_data: 明文原始数据
        :return: 加密后的数据"""

    def encrypt(self, origin_data: typing.Union[str, bytes]) -> bytes:
        """使用指定的加密方法对原始数据进行RSA加密
        :param origin_data: 明文原始数据
        :return: 加密后的数据"""

    def decrypt(self, data: typing.Union[str, bytes]) -> bytes:
        """使用指定的解密方法对密文数据进行RSA解密
        :param data:加密数据
        :return:解密后的数据流"""

    def decrypt_by_e_n(self, data: typing.Union[str, bytes]) -> bytes:
        """RSA 私钥解密 TODO 还未实现，经常报错
        :param data: 密文数据
        :return:  解密后的字节流"""

    def decrypt_by_private(self, data: typing.Union[str, bytes]) -> bytes:
        """RSA 私钥解密
        :param data: 密文数据
        :return:  解密后的字节流"""

    def rsa_private_sign(
        self, origin_data: typing.Union[str, bytes], method="MD5"
    ) -> bytes:
        """rsa私钥生成签名
        3. 私钥制作签名，公钥验证签名:
        使用私钥生成签名，并没有对数据进行加密，另一方在获取数据后，可以利用签名进行验证，
        如果数据传输的过程中被篡改了，那么签名验证就会失败。你可能已经想到了一种可能性，原始数据被篡改了，
        签名也同时被篡改了，这样验证就通过了。
        如果这种情况真的发生了，就说明篡改数据的人已经获取了私钥并利用私钥对篡改后的数据生成新的签名，
        否则，绝没有可能在没有私钥的情况下准确的篡改签名还能通过验证。如果篡改者能够获取私钥这种高度机密的信息，
        那么，防篡改已经没有意义了，因为人家已经彻底攻破了你的系统。

        :param origin_data: 明文数据
        :param method: 签名方法 'MD5', 'SHA-1','SHA-224', SHA-256', 'SHA-384' or 'SHA-512'
        :return:"""

    def rsa_public_verify_sign_by_pkcs1_openssl_pem(
        self, signature: bytes, origin_data: typing.Union[str, bytes]
    ):
        """rsa 以-----BEGIN PUBLIC KEY-----开头的公钥验证签名
        :param signature: rsa原始签名字节流
        :param origin_data: 明文数据
        :return:"""

    def rsa_public_verify_sign_by_pkcs1(
        self, signature: bytes, origin_data: typing.Union[str, bytes]
    ):
        """rsa 以-----BEGIN RSA PUBLIC KEY-----开头的公钥验证签名
        :param signature: rsa原始签名字节流
        :param origin_data: 明文数据
        :return:"""

    @staticmethod
    def generate_pkcs1_keys(
        nbits: int = 2048, format_="PEM"
    ) -> typing.Tuple[bytes, bytes]:
        """生成以-----BEGIN RSA PUBLIC KEY-----开头的公钥字符串和私钥字符串
        @param nbits: 表示可以加密的字符串长度，可以是512,1024,2048,4096等等，不过数字越大生成的速度越慢越安全
        @param format_: 生成key的格式，可以是PEM或PKCS#1 DER 格式，默认PEM格式"""

    @staticmethod
    def generate_pkcs1_openssl_pem_keys(
        nbits: int = 2048, format_="PEM"
    ) -> typing.Tuple[bytes, bytes]:
        """生成以-----BEGIN PUBLIC KEY-----开头的公钥字符串和私钥字符串
        @param nbits: 表示可以加密的字符串长度，可以是512,1024,2048,4096等等，不过数字越大生成的速度越慢越安全
        @param format_: 生成key的格式，可以是PEM或PKCS#1 DER 格式，默认PEM格式"""

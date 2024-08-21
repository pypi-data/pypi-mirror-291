import os
from hashlib import md5
import ddddocr
import requests
from loguru import logger

CHAOJIYING_USERNAME = "dsfdsf"
CHAOJIYING_PASSWORD = "zxcdsf789"
CHAOJIYING_SOFT_ID = "902220"
CHAOJIYING_CODE_TYPE = 1902


class ChaoJiYingClient:
    """
    超级鹰识别服务
    """

    def __init__(self, username: str, password: str, soft_id: str):
        """:param username: 超级鹰账户名
        :param password: 超级鹰密码
        :param soft_id: 超级鹰软件id，用户中心>>软件ID 生成一个替换 soft_id"""

    def post_pic_to_server(self, im: bytes, code_type: str) -> dict:
        """上传图片到超级鹰api进行识别
        :param im:图片字节
        :param code_type: 验证码类型 参考 http://www.chaojiying.com/price.html
        :return: 打码结果json


        错误：{'err_no': -3002, 'err_str': '系统超时', 'pic_id': '2258617500326750295', 'pic_str': '', 'md5': ''}
        # 识别大约6秒
        成功：{'err_no': 0, 'err_str': 'OK', 'pic_id': '1258617520326750296', 'pic_str': '4193', 'md5': '3999eb574db25529d4d6359ab7dd7b82'}
        """

    def report_error_to_server(self, im_id: str) -> dict:
        """验证码识别失败时，向超级鹰提交错误
        :param im_id: 报错验证码的图片ID
        :return:"""


import pytesseract
from PIL import Image
import cv2


class OpencvOcrClient:
    """
    基于opencv ocr的识别服务
    """

    def handle_interference_point(self, img, filename: str):
        """噪点处理"""

    def recognize(self):
        """进行识别
        @return:"""


class TesseractOcrClient:
    """
    基于tesseract ocr的识别服务
    """

    def recognize(self):
        """进行识别
        @return:"""


class BaseRecognizeServer:
    """
    识别服务基类，规范各个识别服务统一接口，对外提供统一服务，
    主要包括识别类型与识别结果的统一
    """

    def __init__(self): ...


class RecognizeHelper:
    """
    识别助手，使用各种识别服务，帮助客户端快速识别验证码

    流程：客户端选择识别模块，输入图片地址或者图片字节流和图片类型，返回识别后的结果
    """

    def __init__(self): ...

    def recognize_img_by_ddddocr(self, img_content: bytes, code_type="1902") -> dict:
        """初始化ddddocr识别服务,由ddddocr识别验证码
        @return:
        2024-08-03 10:33:32.132 | INFO     | __main__:recognize_img:150 - 开始进行识别
        2024-08-03 10:33:32.568 | INFO     | __main__:recognize_img:157 - 识别完成
        aJ93"""

    def recognize_img_by_chaojiying(self, img_content: bytes, code_type="1902") -> dict:
        """初始化chaojiying识别服务, 由chaojiying识别验证码
        @return:
        2024-08-03 10:19:00.855 | INFO     | __main__:recognize_img:153 - 开始进行识别
        {'err_no': 0, 'err_str': 'OK', 'pic_id': '1258710190326750297', 'pic_str': '4j93', 'md5': '532bb7969ff63725cbbf14c5123bb2a7'}
        2024-08-03 10:19:07.114 | INFO     | __main__:recognize_img:160 - 识别完成"""

    def recognize_img(
        self, img_content: bytes, recognize_server="ddddocr", code_type="1902"
    ) -> dict:
        """使用指定识别服务识别验证码图片，获取识别结果
        :param img_content: 验证码图片字节流
        :param recognize_server: 识别服务，会内部映射到对应识别服务对象; dd/cjy
        :param code_type: 验证码类型, 在超级鹰中 1902表示常见4~6位英文数字
        :return:"""

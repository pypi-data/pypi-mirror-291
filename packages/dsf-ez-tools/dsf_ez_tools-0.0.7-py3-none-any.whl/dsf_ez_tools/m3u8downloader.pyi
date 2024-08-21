import os
import platform
import re
import shutil
import subprocess as sp
import time
import typing
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED
from hashlib import md5
from threading import RLock
from urllib.parse import urljoin, urlparse
import psutil
import requests
from Crypto.Cipher import AES
from loguru import logger
from retrying import retry

requests.packages.urllib3.disable_warnings()


class M3U8Parser:

    def __init__(self, m3u8_url, m3u8_content): ...

    def parse_m3u8_content(self) -> dict:
        """解析原始m3u8的内容"""

    def get_max_key(self, discontinuity_index_segment_ls: dict):
        """discontinuity_index_segment_ls={2:[],4:[]}
        获取列表最长的key"""

    def get_max_bandwidth_m3u8_url(self) -> typing.Union[str, None]:
        """通过Master Playlist内容得到最高清的 Media Playlist url"""

    @staticmethod
    def extract_valid_lines(raw_text: str) -> typing.List[str]:
        """# 去除无效行(空行、以#开头的注释)保留 URI行、以#EXT开头的标签（区分大小写）"""

    @staticmethod
    def get_abs_url(relative_url: str, current_abs_m3u8_url: str) -> str:
        """任何相对 URI 都被认为是相对于
        包含它的播放列表的 URI。"""

    def get_next_media_segment(self, index: int) -> tuple:
        """获取当前索引下一个媒体片段index,uri"""

    def parse_ext_x_byterange_line(self, line: str) -> tuple:
        """解析该行内容
        #EXT-X-BYTERANGE:82112@12345"""

    def parse_ext_x_key_line(self, line: str) -> tuple:
        """解析改行内容
        #EXT-X-KEY:METHOD=AES-128,URI="http://test.com",IV=0x9e7aaacac3e30732d4104caba7e9cff0
        """

    def parse_ext_x_map_line(self, line: str) -> tuple:
        """解析该行内容
        ##EXT-X-MAP:URI="init-v1-a1.mp4",BYTERANGE="1000@2000\" """

    @staticmethod
    def get_tag_index(
        segment_index: int, tag_index_map: dict
    ) -> typing.Union[int, None]:
        """获取对当前segment产生作用的tag索引：如key、map"""


class Headers:
    xet = {
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Origin": "https://appli0n8byd8759.h5.xiaoeknow.com",
        "Pragma": "no-cache",
        "Referer": "https://appli0n8byd8759.h5.xiaoeknow.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6304051b)",
        "sec-ch-ua": '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
    }
    cg_51 = {
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "sec-ch-ua": '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    }
    normal = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-language": "zh-CN,zh;q=0.9",
        "upgrade-insecure-requests": "1",
        "accept-encoding": "gzip, deflate, br",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
    }
    x8 = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "sec-ch-ua": '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    }


class _Default:
    NONE = None

    def __bool__(self): ...


class Downloader:
    lock = RLock()

    def __init__(
        self,
        m3u8_url: str,
        video_name: str = "测试电影名",
        cache_path_dir=_Default.NONE,
        video_storage_dir=_Default.NONE,
        m3u8_storage_dir=_Default.NONE,
        default_storage_root_dir="D:\\video_data\\",
        video_name_suffix="mp4",
        save_mode="normal",
        test_download_num=0,
        max_workers=_Default.NONE,
        dec_func=_Default.NONE,
        headers=Headers.normal,
        **kwargs
    ):
        """:param m3u8_url:
        :param video_name: 视频名称
        :param cache_path_dir:  临时缓存目录,用于存储ts文件
        :param video_storage_dir: 视频存储目录
        :param m3u8_storage_dir: 下载的m3u8文件存储目录
        :param default_storage_root_dir:  默认文件存储的根路径 不使用 / 是因为执行cmd时这个会抛出异常
        :param video_name_suffix: 视频文件后缀
        :param save_mode: 存储模式 normal：视频存在则跳过   rewrite：视频存在依然覆盖
        :param test_download_num: 测试下载segmeng数量
        :param max_workers: 最大并发线程数
        :param dec_func:
        :param headers: 请求头"""

    def init_save_path(self):
        """初始化各种存储路径。理想存储格式 ：
        root:[D:
        ideo_data]
            +--测试电影名.mp4
            +--测试电影名_cache
            |      +--Master_Playlist.m3u8
            |      +--Media_Playlist.m3u8
            |      +--000001.ts"""

    @retry(
        stop_max_attempt_number=5, retry_on_result=lambda x: x is None, wait_fixed=2000
    )
    def fetch(self, url: str, is_binary=False) -> typing.Union[bytes, str, None]:
        """通过url请求得到ts、m3u8文件响应"""

    def get_m3u8_content(self) -> str:
        """获取m3u8内容"""

    def request_single_ts(self, ts_url: str) -> bytes:
        """请求单个ts"""

    def decrypt_single_ts(
        self, raw_data: bytes, key_map: dict, segment_index: int
    ) -> bytes:
        """使用key iv解密当前ts内容"""

    def save_single_ts(self, content: bytes, file_name: str):
        """保存ts内容到本地"""

    def load_m3u8(self) -> str: ...

    def load_online_m3u8(self) -> str:
        """加载线上m3u8文件得到其内容"""

    def load_local_m3u8(self) -> str:
        """加载本地m3u8文件得到其内容"""

    def get_key(self, key_url: str) -> bytes:
        """通过key_url 得到 16字节key"""

    @staticmethod
    def get_decipher(key, iv): ...

    def download_decode_save_video(
        self, m3u8_parse_result: dict, media_segment_url: str, segment_index: int
    ):
        """下载、解码、保存视频"""

    def get_initheads_content_map(self, m3u8_parse_result: dict):
        """获取line index与视频头bytes的映射"""

    def download_all_videos(self, m3u8_parse_result: dict):
        """下载所有视频片段"""

    def is_disk_full(self): ...

    def main(self): ...

    def merge_video_file(self):
        """合并视频片段"""

    def win_merge(self) -> bool:
        """Windows平台合并视频，返回是否成功合并"""

    @staticmethod
    def clear_title(title: str) -> str:
        """清洗电影标题成符合window文件名规则"""


def get_test_m3u8_url():
    """获取需要测试的url"""

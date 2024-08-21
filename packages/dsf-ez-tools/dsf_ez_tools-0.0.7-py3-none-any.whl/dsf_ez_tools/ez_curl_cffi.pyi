import logging
import random
import typing
from curl_cffi import requests as curl_cffi_requests
from curl_cffi.requests.models import Response
from loguru import logger
from retrying import retry

impersonate_list = ["chrome100", "chrome100", "chrome104", "chrome107", "chrome110"]


def requests_connect(
    url: str,
    method: str = "GET",
    retry_times: int = 3,
    headers: dict = None,
    data: typing.Union[str, dict] = None,
    cookies: dict = None,
    json: dict = None,
    verify: bool = False,
    proxies: dict = None,
    timeout: typing.Union[int, tuple] = None,
    impersonate: str = "chrome110",
    random_client: bool = False,
    **requests_kwargs
) -> Response:
    """对requests请求进行指定次数重试
    :param url:
    :param method:
    :param retry_times: 异常重试次数
    :param headers:
    :param data:
    :param cookies:
    :param json:
    :param verify:
    :param proxies:
    :param timeout:
    :param impersonate:
    :param random_client:  是否随机浏览器jar指纹
    :param requests_kwargs:   requests其他请求参数
    :return: 请求成功返回 Response，请求失败返回None"""

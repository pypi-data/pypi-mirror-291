import logging
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from retrying import retry
from loguru import logger
import typing


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
    **requests_kwargs
) -> requests.Response:
    """对requests请求进行指定次数重试
    @param url:
    @param method:
    @param retry_times: 异常重试次数
    @param requests_kwargs: requests请求参数
    @return:"""

import json
from datetime import datetime
from loguru import logger
from ez_requests import requests_connect


class DingtalkRobot:

    def __init__(self, web_hook_url: str, phone: str, keyword: str):
        """@param web_hook_url: 机器人回调地址
        @param phone: 需要@的手机号
        @param keyword:  触发回调的关键词"""

    def send_markdown_message(self, title: str, mk_text: str) -> None:
        """发送markdown文本到钉钉
        @param title: 主题名  str
        @param mk_text: 钉钉内容，必须包含机器人设置的关键词"""

    def send_text_message(self, text: str) -> None:
        """发送text文本到钉钉
        @param text: 钉钉内容  str"""

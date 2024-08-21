import os
import subprocess
import time
import traceback
from loguru import logger
from py_mini_racer import MiniRacer


class Popen(subprocess.Popen):

    def __init__(self, *args, **kwargs): ...


subprocess.Popen = Popen
import execjs
from execjs._abstract_runtime import AbstractRuntime
from execjs._abstract_runtime_context import AbstractRuntimeContext


class ExecjsUtils:
    """
    使用 execjs 调用js，使用 set_execjs_runtime 切换js运行时
    """

    def __init__(self, is_debugger=False): ...

    def compile_from_file(self, js_file_path: str, cwd=None) -> None:
        """从文件中读取js并进行编译
        :param cwd: JS中使用了其他模块如jsdom时，要么在当前目录下npm install jsdom，要么通过cwd指定模块所在目录路径；
        cwd="C:/Users/AppData/Roaming/npm/node_modules\" """

    def compile_from_string(self, js_code_string: str) -> None:
        """直接编译js字符串"""

    def set_execjs_runtime(self, runtime="Node") -> AbstractRuntime:
        """设置 js runtime
        :param runtime: Node、PyV8、JScript等"""

    def call(self, *args, **kwargs): ...


class V8ExecjsUtils:
    """
    py_mini_racer是一个python绑定了Google V8引擎的库可以基于V8环境执行JS
    eval：默认返回最后一条语句执行结果； 每次执行会持久化影响到上下文环境；
    call：内部只是拼接JS调用代码，然后执行eval，再处理下返回值；
    """

    def __init__(self, is_debugger=False):
        """:param js_file_path:待执行的JS文件路径"""

    def compile_from_file(self, js_file_path: str) -> None:
        """会在v8内存中加载这段js代码，然后运行"""

    def compile_from_string(self, js_code_string: str) -> None:
        """会在v8内存中加载这段js代码，然后运行"""

    def call(self, *args, **kwargs):
        """按如下格式执行： fun('js_funName', param1,param2)，
        在MiniRacer内部会在上面eval的基础上再运行函数调用获取返回值，效率非常高"""


def __run_speed(func: callable, times=100):
    """测试调用函数指定次数花费的时间"""

"""
    Module: AIHCArgumentParser
"""
import argparse
import sys as _sys
import os
from pathlib import Path

config_dir = Path('~/.aihc').expanduser()
config_file = config_dir / 'config'

class AIHCArgumentParser(argparse.ArgumentParser):
    """AIHC命令行解析器"""
    def print_help(self, file=None):
        """
            打印帮助信息到指定文件或默认输出流中。
        如果未提供文件，则将帮助信息写入默认输出流（通常是标准输出）。
        
        Args:
            file (Optional[TextIO], optional): 要写入的文件对象（默认为None，表示默认输出流）. Defaults to None.
        
        Returns:
            None: 无返回值，直接将帮助信息写入指定文件或默认输出流。
        """
        if file is None:
            file = _sys.stdout

        base_dir = os.path.dirname(os.path.abspath(__file__))
        with open(base_dir + '/doc/help_message.txt', 'r', encoding='utf-8') as help_file:
            message = help_file.read()
            
        file.write(message + "\n")

    def print_job_help(self, file=None):
        """
            打印作业的帮助信息，默认输出到标准输出。
        如果指定了文件参数，则将帮助信息写入该文件中。
        
        Args:
            file (Optional[TextIO], optional): 可选参数，默认为None，表示输出到标准输出。其他类型的文件对象也可以指定。 Default value is None.
        
        Returns:
            None: 无返回值，直接在给定的文件或标准输出上输出帮助信息。
        """
        if file is None:
            file = _sys.stdout

        base_dir = os.path.dirname(os.path.abspath(__file__))
        with open(base_dir + '/doc/job_help_message.txt', 'r', encoding='utf-8') as help_file:
            message = help_file.read()

        file.write(message + "\n")

    def print_pool_help(self, file=None):
        """
            打印关于池的帮助信息。如果未指定文件，则默认为标准输出。
        参数：
            file (Optional[TextIO], optional): 要写入的文件对象（默认为None）. Defaults to None.
        Returns:
            None: 无返回值，直接将帮助信息写入给定的文件或标准输出。
        """
        if file is None:
            file = _sys.stdout

        base_dir = os.path.dirname(os.path.abspath(__file__))
        with open(base_dir + '/doc/pool_help_message.txt', 'r', encoding='utf-8') as help_file:
            message = help_file.read()

        file.write(message + "\n")

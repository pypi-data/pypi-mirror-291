#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
# from __future__ import absolute_import, print_function, division
# ----------------------------------------------------------------
# File Name:        file_object.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      Main Function: 定义“文件”相关的函数和类。
#                   Outer Parameters: xxxxxxx
# Class List:       xxxxxxx
# Function List:    xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
# History:
#        <author>        <version>        <time>        <desc>
#       Jiwei Huang        0.0.1         2012/01/01     create
#       Jiwei Huang        0.0.1         2024/05/30     revise
#       Jiwei Huang        0.0.1         2024/06/11     revise
#       Jiwei Huang        0.0.1         2024/07/31     revise
#       Jiwei Huang        0.0.1         2024/08/20     finish
# ----------------------------------------------------------------
# 导包 ============================================================
import inspect
import os.path
import sys
from typing import Optional, Union

# chardet库需要安装：pip install chardet
import chardet

# 声明 ============================================================
__version__ = "0.0.1"
__author__ = "Jiwei Huang"
__doc__ = """
Defining functions and classes associated with file.
"""
__all__ = [
    'get_file_encoding_chardet',
    'file_info',
    'get_file_info',
    'get_file_info_of_module',
    'get_file_object',
    'FileInfo',
    'FileObject',
]


# 定义 ===============================================================
# noinspection PyBroadException
def get_file_encoding_chardet(file_path):
    """
    利用chardet库获取文件的编码。

    :param file_path: 文件的完整路径。
    :return: 文件的编码，任何失败都将返回None。
    """
    if os.path.exists(file_path) and os.path.isfile(file_path):
        try:
            with open(file_path, 'rb') as f:
                result = chardet.detect(f.read())
                encoding = result['encoding']
                return encoding
        except Exception:
            return None
    else:
        return None


def file_info(directory_path: str, base_name: str,
              ext_name: Optional[str] = None,
              encoding: Optional[str] = None,
              **kwargs):
    """
    构造文件信息对象。

    :param directory_path: 文件所在目录的路径。
    :param base_name: 文件基名。
    :param ext_name: 文件扩展名（不含`.`），缺省为None。
    :param encoding: 文件编码，缺省为None。
    :param kwargs: 有关文件的其他信息，将被转化为对象属性。
    :return: FileInfo对象。
    """
    return FileInfo(directory_path, base_name,
                    ext_name, encoding,
                    **kwargs)


def get_file_info(file_path: str, encoding: Optional[str] = None,
                  **kwargs):
    """
    获取文件信息对象。

    :param file_path: 文件的完整路径。
    :param encoding: 文件编码，缺省为None。
    :param kwargs: 有关文件的其他信息，将被转化为对象属性。
    :return: FileInfo对象。
    """
    directory_path, file_name = os.path.split(file_path)
    base_name, ext_name = os.path.splitext(file_name)
    return FileInfo(directory_path, base_name, ext_name,
                    encoding, **kwargs)


def get_file_info_of_module(mod_name):
    """
    利用inspect获取指定模块名的文件信息。

    :param mod_name: 指定的模块名。
    :return: FileInfo对象。
    """
    file_path = inspect.getfile(sys.modules[mod_name])
    return get_file_info(file_path)


def get_file_object(file: str, encoding: Optional[str] = None, **kwargs):
    """
    获取文件对象。

    :param file: 文件的路径或文件信息对象。
    :param encoding: 文件编码。
    :param kwargs: 其他可选关键字参数，这些参数全部转化为对象的属性。
    :return: FileObject对象。
    """
    return FileObject(file, encoding=encoding, **kwargs)


# -----------------------------------------------------------------
class FileInfo(object):
    """
    类`FileInfo`用于承载”文件信息“。
    """

    def __init__(self, directory_path: str, base_name: str,
                 ext_name: Optional[str] = None,
                 encoding: Optional[str] = None,
                 **kwargs):
        """
        类`FileInfo`的初始化方法。

        :param directory_path: 文件所在的目录路径。
        :param base_name: 文件基名。
        :param ext_name: 文件扩展名（不含`.`），
                        如果包含`.`,在内部将其删除，缺省为None。
        :param encoding: 文件编码，缺省为None。
        :param kwargs: 有关文件的其他信息，将被转化为对象属性。
        """
        self.__directory_path = directory_path
        self.__base_name = base_name
        self.__ext_name = ext_name

        # 如果文件扩展名包含点，则将点删除。
        if self.__ext_name.startswith('.'):
            self.__ext_name = self.__ext_name[1:]

        # 构建文件名。
        if ext_name is not None:
            self.__name = "{}.{}".format(
                self.__base_name,
                self.__ext_name)
        else:
            self.__name = self.__base_name

        # 构建文件的路径。
        self.__path = os.path.join(self.__directory_path,
                                   self.__name)

        # 尝试获取文件的编码。
        self.__encoding = encoding
        if self.__encoding is None:
            self.__encoding = get_file_encoding_chardet(self.__path)

        # 其他关键字参数被转换为对象的属性。
        for key in kwargs.keys():
            if not hasattr(self, key):
                setattr(self, key, kwargs[key])

    @property
    def directory_path(self) -> str:
        """
        获取文件所在目录的路径。

        :return: 文件所在目录的路径。
        """
        return self.__directory_path

    @property
    def base_name(self) -> str:
        """
        获取文件基名。

        :return: 文件基名。
        """
        return self.__base_name

    @property
    def ext_name(self) -> Optional[str]:
        """
        获取文件扩展名（不含`.`）。

        :return: 文件扩展名（不含`.`）。
        """
        return self.__ext_name

    @property
    def name(self) -> str:
        """
        获取文件名。

        :return: 文件名。
        """
        return self.__name

    @property
    def path(self) -> str:
        """
        获取文件的路径。

        :return: 文件的路径。
        """
        return self.__path

    @property
    def encoding(self) -> Optional[str]:
        """
        获取文件编码。

        :return: 文件编码。
        """
        return self.__encoding

    @encoding.setter
    def encoding(self, new_encoding: str):
        """
        设置文件编码。

        :param new_encoding: 新的文件编码。
        :return: None
        """
        self.__encoding = new_encoding

    def make_directory(self):
        """
        创建文件目录

        :return: None
        """
        if not os.path.exists(self.directory_path):
            os.makedirs(self.directory_path, exist_ok=True)

    def make_file(self):
        """
        创建文件。

        :return: None
        """
        self.make_directory()
        if not os.path.exists(self.path):
            open(self.path, "w").close()

    def __eq__(self, other):
        """
        重载`==`操作符。

        :param other: 另一个FileInfo对象。
        :return: 相等返回True，否则返回False。
        """
        if isinstance(other, FileInfo):
            if self.path == other.path:
                return True
        else:
            return False

    def __ne__(self, other):
        """
        重载`!=`操作符。

        :param other: 另一个FileInfo对象。
        :return: 不相等返回True，否则返回False。
        """
        return not self.__eq__(other)

    def __hash__(self):
        """
        获取对象的hash码。

        :return: 对象的hash码。
        """
        result: int = 1
        for arg in (self.directory_path, self.base_name, self.ext_name):
            result = 31 * result + (0 if arg is None else hash(arg))

        return result

    def __str__(self):
        """
        获取对象字符串。

        :return:对象字符串。
        """
        return self.path

    def __repr__(self):
        """
        获取对象的文本式。

        :return:对象的文本式。
        """
        res_dict = dict()
        for key in self.__dict__:
            if key.startswith("_FileInfo__"):
                res_dict[key.removeprefix("_FileInfo__")] = self.__dict__[key]
            else:
                res_dict[key] = self.__dict__[key]
        return "FileInfo{}".format(res_dict)


# -----------------------------------------------------------------
class FileObject(object):
    """
    类`FileObject`表征“文件对象”。
    """

    def __init__(self, file: Union[str, FileInfo],
                 encoding: Optional[str] = None,
                 **kwargs):
        """
        类`FileObject`的初始化方法。

        :param file: 文件的路径或文件信息对象。
        :param encoding: 文件编码。
        :param kwargs: 其他可选关键字参数，这些参数全部转化为对象的属性。
        """
        if isinstance(file, str):
            self.__file_full_path = file
            # 分离文件的路径、文件名和文件扩展名。
            (self.__file_path, self.__file_full_name) = \
                os.path.split(self.__file_full_path)
            (self.__file_base_name, self.__file_ext_name) = \
                os.path.splitext(self.__file_full_name)
            self.__file_ext_name = self.__file_ext_name.strip()
            # 如果文件扩展名包含点，则将点删除。
            if self.__file_ext_name.startswith('.'):
                self.__ext_name = self.__file_ext_name[1:]
        else:
            self.__file_full_path = file.path
            self.__file_path = file.directory_path
            self.__file_full_name = file.name
            self.__file_base_name = file.base_name
            self.__file_ext_name = file.ext_name
            for key in file.__dict__:
                if not key.startswith("_FileInfo__"):
                    if not hasattr(self, key):
                        setattr(self, key, file.__dict__[key])

        # 尝试获取文件的编码。
        self.__encoding = encoding
        if self.__encoding is None:
            self.__encoding = get_file_encoding_chardet(self.__file_full_path)

        # 其他关键字参数被转换为对象的属性。
        for key in kwargs.keys():
            if not hasattr(self, key):
                setattr(self, key, kwargs[key])

    @property
    def file_full_path(self) -> str:
        """
        获取文件的完整路径。

        :return: 文件的完整路径。
        """
        return self.__file_full_path

    @property
    def file_path(self) -> str:
        """
        获取文件所在目录的完整路径。

        :return: 文件所在目录的完整路径。
        """
        return self.__file_path

    @property
    def file_full_name(self) -> str:
        """
        获取文件的完整文件名（包含扩展名）。

        :return: 文件的完整文件名（包含扩展名）。
        """
        return self.__file_full_name

    @property
    def file_base_name(self) -> str:
        """
        获取文件的基文件名（不包含扩展名）。

        :return: 文件的基文件名（不包含扩展名）。
        """
        return self.__file_base_name

    @property
    def file_ext_name(self) -> str:
        """
        获取文件的扩展名（不包含‘.’）。

        :return: 文件的扩展名（不包含‘.’）。
        """
        return self.__file_ext_name

    @property
    def encoding(self) -> Optional[str]:
        """
        获取文件编码。

        :return: 文件编码。
        """
        return self.__encoding

    @encoding.setter
    def encoding(self, new_encoding: str):
        """
        设置文件编码。

        :param new_encoding: 新的文件编码。
        :return: None
        """
        self.__encoding = new_encoding

    def to_file_info(self) -> FileInfo:
        """
        将其文件对象转换为文件信息对象。

        :return: 文件信息对象。
        """
        return FileInfo(self.file_path, self.file_base_name, self.file_ext_name)

    def make_directory(self):
        """
        创建文件目录

        :return: None
        """
        if not os.path.exists(self.file_path):
            os.makedirs(self.file_path, exist_ok=True)

    def make_file(self):
        """
        创建文件。

        :return: None
        """
        self.make_directory()
        if not os.path.exists(self.file_full_path):
            open(self.file_full_path, "w").close()

    def __eq__(self, other):
        """
        重载`==`操作符。

        :param other: 另一个FileObject对象。
        :return: 相等返回True，否则返回False。
        """
        if isinstance(other, FileObject):
            if self.file_full_path == other.file_full_path:
                return True
        else:
            return False

    def __ne__(self, other):
        """
        重载`!=`操作符。

        :param other: 另一个FileObject对象。
        :return: 不相等返回True，否则返回False。
        """
        return not self.__eq__(other)

    def __hash__(self):
        """
        获取对象的hash码。

        :return: 对象的hash码。
        """
        result: int = 1
        for arg in (self.file_path, self.file_base_name, self.file_ext_name):
            result = 31 * result + (0 if arg is None else hash(arg))

        return result

    def __str__(self):
        """
        获取对象字符串。

        :return:对象字符串。
        """
        return self.file_full_path

    def __repr__(self):
        """
        获取对象的文本式。

        :return:对象的文本式。
        """
        res_dict = dict()
        for key in self.__dict__:
            if key.startswith("_FileObject__"):
                res_dict[key.removeprefix("_FileObject__")] = self.__dict__[key]
            else:
                res_dict[key] = self.__dict__[key]
        return "FileObject{}".format(res_dict)
# =================================================================

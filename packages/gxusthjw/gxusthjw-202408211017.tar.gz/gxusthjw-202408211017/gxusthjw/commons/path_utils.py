#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
# from __future__ import absolute_import, print_function, division
# ------------------------------------------------------------------
# File Name:        path_utils.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      Main Function: 为"路径"提供辅助方法或类。
#                   Outer Parameters: xxxxxxx
# Class List:       xxxxxxx
# Function List:    xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
# History:
#        <author>        <version>        <time>        <desc>
#       Jiwei Huang        0.0.1         2012/01/01     create
#       Jiwei Huang        0.0.1         2023/10/30     revise
#       Jiwei Huang        0.0.1         2024/01/01     revise
#       Jiwei Huang        0.0.1         2024/06/11     revise
#       Jiwei Huang        0.0.1         2024/07/31     revise
#       Jiwei Huang        0.0.1         2024/08/20     revise
# ------------------------------------------------------------------
# 导包 =============================================================
import fnmatch
import os

from typing import Optional

# 声明 =============================================================
__version__ = "0.0.1"
__author__ = "Jiwei Huang"
__doc__ = """
Defining the classes and functions for path.
"""
__all__ = [
    'join_file_path',
    'sep_file_path',
    'list_files_with_suffix',
    'print_files_and_folders',
    'print_top_level_files_and_folders',
    'list_top_level_files_and_folders',
]


# 定义 ================================================================

def join_file_path(path: str, file_base_name: str,
                   file_type: str = '', suffix="_副本") -> str:
    """
    将文件路径、文件名和文件类型结合为完整的文件路径。

    如果文件的完整路径下已存在指定的文件，则在文件名后加“_副本”。

    该方法并不实际创建文件，只是链接文件路径。

    :param path: 路径。
    :param file_base_name: 文件名（不含扩展名）。
    :param file_type: 文件类型（即文件的扩展名，含“.”），如果不包含“.”，则自动添加“.”。
    :param suffix: 后缀。
    :return: 完整的文件路径。
    """
    if not file_type.startswith("."):
        file_type = ".{}".format(file_type.strip())
    path_file = path + os.sep + file_base_name + file_type
    if os.path.exists(path_file):
        return join_file_path(path, file_base_name + suffix, file_type)
    else:
        return path_file


def sep_file_path(file, with_dot_in_ext=True):
    """
    获取指定文件路径的文件名和父目录。

    :param file: 文件完整路径。
    :param with_dot_in_ext: 指定返回的文件扩展名中是否包含“.”，
                            如果为True，则包含，否则不包含。
    :return: (文件父目录, 文件基名，文件扩展名)
    """
    filepath, temp_file_name = os.path.split(file)
    filename, file_ext = os.path.splitext(temp_file_name)
    if not with_dot_in_ext:
        file_ext = file_ext.replace(".", " ").strip()
    return filepath, filename, file_ext


def list_files_with_suffix(suffix: str = '.csv',
                           path: Optional[str] = None):
    """
    列出指定路径下指定文件后缀名的所有文件。

    :param suffix: 指定的文件后缀名。
    :param path: 指定的路径。
    :return: 文件列表。
    :rtype: list
    """
    if path is None:
        path = os.getcwd()
    if os.path.isfile(path):
        path = os.path.dirname(path)
    # 使用 os.listdir() 获取当前目录下的所有文件和子目录
    files_in_current_dir = os.listdir(path)
    # 使用 fnmatch 来过滤出符合特定后缀的文件
    matching_files = fnmatch.filter(files_in_current_dir, f'*{suffix}')
    return [os.path.join(path, file) for file in matching_files]


def print_files_and_folders(directory: str):
    """
    遍历输出指定目录下所有子目录和文件。

    :param directory: 指定的目录。
    """
    # 使用os.walk遍历目录
    for root, dirs, files in os.walk(directory):
        print(f"Directory: {root}")
        print("Subdirectories:")
        for __dir in dirs:
            print(f"\t{__dir}")
        print("Files:")
        for file in files:
            print(f"\t{file}")
        print("-" * 40)


def print_top_level_files_and_folders(directory: str):
    """
    遍历输出指定目录下所有顶级子目录和文件。

    :param directory: 指定的目录。
    """
    # 使用os.listdir获取目录下的所有条目
    entries = os.listdir(directory)

    # 打印目录名
    print(f"Directory: {directory}")

    # 分别打印文件和文件夹
    print("Top-level directories and files:")
    for entry in entries:
        path = os.path.join(directory, entry)
        if os.path.isdir(path):
            print(f"\tDirectory: {entry}")
        else:
            print(f"\tFile: {entry}")


def list_top_level_files_and_folders(directory: str):
    """
    获取输出指定目录下所有顶级子目录和文件。

    :param directory: 指定的目录。
    :return: (top-level directories, top-level files)
    """
    # 使用os.listdir获取目录下的所有条目
    entries = os.listdir(directory)
    folders = [entry for entry in entries if os.path.isdir(os.path.join(directory, entry))]
    files = [entry for entry in entries if not os.path.isdir(os.path.join(directory, entry))]
    return folders, files

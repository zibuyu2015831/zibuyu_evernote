# -*- coding: utf-8 -*-

"""
--------------------------------------------
project: python_test
author: 子不语
date: 2025/3/10
contact: 【公众号】思维兵工厂
description: 
--------------------------------------------
"""

from dataclasses import dataclass


@dataclass
class ImageItem:
    is_url: bool  # 是否是网络图片
    image_name: str  # 图片名称
    image_path: str  # 图片完整路径（如果是本地图片且为相对路径，拼接为绝对路径）
    image_suffix: str  # 图片后缀
    original_text: str = ''  # 原文本
    hash_str: str = ''  # 图片的哈希值
    final_content: str = ''  # 最终的evernote的html内容

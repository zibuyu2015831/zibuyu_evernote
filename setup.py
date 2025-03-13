# -*- coding: utf-8 -*-

"""
--------------------------------------------
project: zibuyu_LLM
author: 子不语
date: 2024/5/11
contact: 【公众号】思维兵工厂
description: 
--------------------------------------------
"""

from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'evernote的官方SDK的个人优化版'
# long_description = DESCRIPTION

with open('./Readme.md', 'r', encoding='utf-8') as file:
    long_description = file.read()

setup(
    name='zibuyu_evernote',
    version=VERSION,
    description='子不语个人工具包-印象笔记SDK',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='子不语',
    packages=find_packages('./zibuyu_evernote'),
    license='MIT',
    package_dir={'': './zibuyu_evernote'},
    keywords=['zibuyu', 'zibuyu_evernote', 'evernote'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12'
    ],
    install_requires=[
        "certifi",
        "charset-normalizer",
        "html2text",
        "httplib2",
        "idna",
        "Markdown",
        "oauth2",
        "oauthlib",
        "pip",
        "Pygments",
        "pyparsing",
        "requests",
        "requests-oauthlib",
        "setuptools",
        "urllib3",
        "wheel",
    ],
    python_requires='>=3.9'
)

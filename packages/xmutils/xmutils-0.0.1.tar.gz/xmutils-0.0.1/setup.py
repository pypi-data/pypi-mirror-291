r'''
Author: Mr Yuan
Date: 2024-07-05
LastEditTime: 2024-08-18
LastEditors: Mr Yuan
FilePath: \xm_utils\setup.py

Description: 

'''
import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
print(here)
# 包基本信息
NAME = 'xmutils'
VERSION = '0.0.1'
DESCRIPTION = 'A Python package developed about common tools.'
AUTHOR = 'Yuan'
EMAIL = '2465359365@qq.com'
URL = 'https://gitee.com/ccutlab/xmutil'
REQUIRES_PYTHON = '>=3.6.0'

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name=NAME,  # 包名
    version=VERSION,    # 版本号
    author=AUTHOR,  # 作者
    author_email=EMAIL,
    description=DESCRIPTION,  # 库描述
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="BSD",
    url=URL,    # 库官方地址
    project_urls={
        "Bug Tracker": "https://gitee.com/ccutlab/xmutil",
    },
    # 命令行
    entry_points={
        "console_scripts": [
            "pxp=xmutils.CommandLine:main"
        ]
    },
    # 包依赖
    install_requires=[

    ],
    # 程序分类信息
    classifiers=[
        "Operating System :: OS Independent",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Text Processing :: Indexing",
        "Topic :: Utilities",
        # 属于什么类型
        "Topic :: Software Development :: Libraries :: Python Modules",
        # 许可信息
        "License :: OSI Approved :: BSD License",
        # 目标Python版本
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    # 指定哪个目录下的文件被映射到哪个源码包
    package_dir={'xmutils': 'src/xmutils'},
    # 需要处理的包目录
    packages=['xmutils'],
    python_requires=REQUIRES_PYTHON,
)

from setuptools import setup, Extension
from Cython.Build import cythonize
import os

# 定义Cython扩展
extensions = [
    Extension(
        "cliquest.cli",  # 模块的名称
        ["cliquest/cli.pyx"],  # Cython 文件路径
        extra_compile_args=["-O2"],  # 优化编译参数
    ),
]

# 设置脚本
setup(
    name="cliquest",
    version="0.2.2",
    author="YN",
    author_email="",
    description="A package for estimating CLI",
    ext_modules=cythonize(extensions),
    packages=["cliquest"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: CPython",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

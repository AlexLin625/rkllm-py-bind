from setuptools import setup, find_packages, Extension
import glob
import os

# 动态查找.so文件
so_files = glob.glob(os.path.join('dist', '*.so'))

# 创建扩展模块列表
ext_modules = [Extension(os.path.splitext(os.path.basename(so))[0], sources=[]) for so in so_files]

setup(
    name="rkllm",
    version="0.0.1",
    description="RKLLM Python Bindings",
    author="a1exlin",
    author_email="me@a1exlin.cn",
    packages=find_packages(where="dist"),
    package_dir={"": "dist"},
    package_data={"": ["*.so", "*.pyi"]},
    include_package_data=True,
    zip_safe=False,
    ext_modules=ext_modules,  # 添加扩展模块
)
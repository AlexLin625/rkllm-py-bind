from setuptools import setup, find_packages, Extension
import glob
import os

# 动态查找.so文件
so_files = glob.glob(os.path.join('dist', '*.so'))

# 确保dist目录中有__init__.py文件
init_file_path = os.path.join('dist', '__init__.py')
if not os.path.exists(init_file_path):
    with open(init_file_path, 'w') as f:
        f.write("# This is an auto-generated file for the rkllm package.\n")

# 确保dist目录中有__init__.pyi文件
init_pyi_file_path = os.path.join('dist', '__init__.pyi')
with open(init_pyi_file_path, 'w') as f:
    f.write("# This is an auto-generated file.\n\nfrom .rkllm import *\n")

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
    package_data={"rkllm": ["*.py", "*.pyi", "*.so"]},  # 确保包含所有需要的文件
    include_package_data=True,
    zip_safe=False,
    ext_modules=ext_modules,  # 添加扩展模块
)
from setuptools import setup, Extension
from Cython.Build import cythonize

# 定义Cython扩展
extensions = [
    Extension("Connnet.network", ["Connnet/network.pyx"]),
]

# 设置脚本
setup(
    name="Connnet",
    version="0.2.2",
    author="YN",
    author_email="",
    description="A network generation package",
    ext_modules=cythonize(extensions),
    packages=["Connnet"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

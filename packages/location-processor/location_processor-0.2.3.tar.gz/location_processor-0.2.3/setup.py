# setup.py

from setuptools import setup, Extension
from Cython.Build import cythonize

# 定义 Cython 扩展
extensions = [
    Extension("location_processor.process_location", ["location_processor/process_location.pyx"]),
]

# 设置脚本
setup(
    name="location_processor",
    version="0.2.3",
    author="Hank",
    description="A package for processing location data",
    ext_modules=cythonize(extensions),
    packages=["location_processor"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: CPython",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

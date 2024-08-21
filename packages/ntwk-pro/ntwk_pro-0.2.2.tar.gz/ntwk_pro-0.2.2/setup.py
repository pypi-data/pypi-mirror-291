from setuptools import setup, Extension
from Cython.Build import cythonize

# 定义所有的Cython扩展
extensions = [
    Extension("ntwk_pro.basic_index_dict", ["ntwk_pro/basic_index_dict.pyx"]),
    Extension("ntwk_pro.create_network", ["ntwk_pro/create_network.pyx"]),
    Extension("ntwk_pro.filter_sequence", ["ntwk_pro/filter_sequence.pyx"]),
    Extension("ntwk_pro.clifin", ["ntwk_pro/clifin.pyx"]),
    Extension("ntwk_pro.find_community_byhost", ["ntwk_pro/find_community_byhost.pyx"]),
]

# 设置脚本
setup(
    name="ntwk_pro",
    version="0.2.2",
    author="CVN",
    author_email="",
    description="",
    ext_modules=cythonize(extensions),
    packages=["ntwk_pro"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: CPython",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

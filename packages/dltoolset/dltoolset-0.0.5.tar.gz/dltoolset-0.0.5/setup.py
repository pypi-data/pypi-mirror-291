from setuptools import setup, find_packages

VERSION = '0.0.5'
DESCRIPTION = 'Deep Learning Utility Library'

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# 配置
setup(
    name="dltoolset",
    version=VERSION,
    author="horiki",
    author_email="qilei.zhou6@gmail.com",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NoyeArk/dltoolset",
    packages=find_packages(),
    install_requires=[],  # add any additional packages that
    # 需要和你的包一起安装，例如：'caer'

    keywords=['python', 'first package'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)

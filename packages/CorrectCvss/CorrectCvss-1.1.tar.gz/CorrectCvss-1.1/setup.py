from setuptools import setup, find_packages


setup(
    name="CorrectCvss",  # 你的包名称
    version="1.1",  # 包的版本号
    author="bole",
    author_email="bobolehe@gmail.com",
    description="Verify the CVSS vector specification and receive JSON data to generate a CVSS vector.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",  # 如果你使用的是Markdown格式的README
    url="https://github.com/bobolehe/CorrectCvss",  # 项目主页URL
    packages=find_packages(),  # 自动查找项目中的包
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',  # 你支持的Python版本
    install_requires=[
        'cvss==3.1',
    ],
)
from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fp:
    long_description = fp.read()

setup(
    name="minifw",
    version="0.0.1",
    description="基于图像识别的自动化黑盒测试框架",
    author="KateTseng",
    author_email="Kate.TsengK@outlook.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NakanoSanku/minidevice",
    license="MIT",
    keywords="Auto Script Testing",
    project_urls={},
    packages=find_packages(),
    include_package_data=True,
    package_data={
        # 如果你的bin文件在minidevice包下，可以这样指定
        'minifw.touch': ['bin/**/*'],
        'minifw.screencap': ['bin/**/*'],
        'minifw.common': ['bin/**/*'],
        # 如果bin文件不在包内，也可以直接指定路径
        # '': ['bin/*'],
    },
    install_requires=["adbutils",
                      "loguru",
                      "requests",
                      'opencv-python',
                      'PyTurboJPEG'
                      ],
    python_requires=">=3",
)
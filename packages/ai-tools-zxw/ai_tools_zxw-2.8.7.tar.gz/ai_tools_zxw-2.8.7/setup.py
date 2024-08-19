from setuptools import setup, find_packages

setup(
    name="ai_tools_zxw",
    version="2.8.7",
    packages=find_packages(),
    install_requires=[
        'xlwt',
        'psutil',
        'ultralytics',
        'opencv-python',
        'matplotlib',
        'tqdm',
        'pycocotools',
        # 讯飞星火大模型依赖的包
        'websocket-client',
        'openpyxl',
        'openai',
        # 依赖的其他包，例如：'requests>=2.0.0'
        # nlp预处理
        'emoji',
        'jieba',
        # Claude大模型
        'anthropic',
        # 闻心一言 大模型
        'qianfan'
    ],
    author="xue wei zhang",
    author_email="",
    description="常用的人工智能操作的中文工具包。",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sunshineinwater/",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

import setuptools


setuptools.setup(
    name="wbase",
    version="0.0.1", # 包版本
    author="Beall", # 用于识别包的作者，下同，可以填写你的信息或者随便填一个
    author_email="ddeb@163.com",
    description="", # 一个简短的包的总结
    long_description="README.md",# 包的详细说明，可以加载前面说的README.md作为长描述，也可以直接输入你的包名称或者任何你想详细说明的内容
    long_description_content_type="", # 告诉索引什么类型的标记用于长描述。在这种情况下，它是Markdown。url是项目主页的URL。对于许多项目，这只是一个指向GitHub，GitLab，Bitbucket或类似代码托管服务的链接。这里也可以直接输入你的包名称
    packages=setuptools.find_packages(), # 应包含在分发包中的所有Python 导入包的列表。我们可以使用 自动发现所有包和子包，而不是手动列出每个包。在这种情况下，包列表将是example_pkg，因为它是唯一存在的包。find_packages()classifiers告诉索引并点一些关于你的包的其他元数据
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

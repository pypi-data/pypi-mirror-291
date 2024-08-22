from setuptools import setup, find_packages

from dnscli.version import version

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="dnscli",
    version=version,
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'alidns=dnscli.cli.alidns:main',
            'dnspod=dnscli.cli.dnspod:main',
        ],
    },
    author="liwanggui",
    author_email="liwanggui@163.com",
    description="域名解析记录管理工具",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/liwanggui/dnscli",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)

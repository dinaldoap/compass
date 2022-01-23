# coding=utf-8
from setuptools import setup, find_packages

setup(
    name="compass",
    version="0.1.0",
    license="",
    description="Helping investors to stick with theirs plans.",
    url="",
    platforms="Linux",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    author="",
    author_email="",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "compass = compass.__main__:main",
            "compass-report = compass.__main__:report",
        ]
    },
    install_requires=[
        "numpy==1.20.2",
        "pandas==1.2.3",
        "openpyxl==3.0.7",
        "requests==2.25.1",
        "lxml==4.6.3",
        "babel==2.9.1",
    ],
    python_requires=">=3.8",
    zip_safe=True,
)

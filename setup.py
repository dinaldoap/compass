# coding=utf-8
from setuptools import setup, find_packages


def get_install_requires():
    with open("requirements-prod.lock", encoding="utf-8") as file:
        content = file.read()
    return content.split()


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
        ]
    },
    install_requires=get_install_requires(),
    python_requires=">=3.8",
    zip_safe=True,
)

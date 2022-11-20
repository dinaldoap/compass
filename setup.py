"""Setup.py."""
import re

from setuptools import find_packages, setup


def _get_install_requires():
    with open("requirements-prod.txt", encoding="utf-8") as file:
        content = file.read()
    deps = content.split("\n")
    deps = [dep for dep in deps if re.match(r"^\w", dep)]
    return deps


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
    install_requires=_get_install_requires(),
    python_requires=">=3.8",
    zip_safe=True,
)

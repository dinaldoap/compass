"""Setup.py."""
from setuptools import find_packages, setup

setup(
    name="compass",
    version="0.1.0",
    license="",
    description="Leading investors to theirs targets.",
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
    python_requires=">=3.8",
    zip_safe=True,
)

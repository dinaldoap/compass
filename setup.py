# coding=utf-8
from setuptools import setup, find_packages

setup(name='template',
      version='0.1.0',
      license='',
      description='template.',
      url='',
      platforms='Linux',
      classifiers=[
          'Programming Language :: Python :: 3',
      ],
      author='',
      author_email='',
      packages=find_packages(),
      entry_points={
          'console_scripts': [
              'template = template.main:main',
          ]
      },
      install_requires=['numpy==1.20.2',
                        'pandas==1.2.3',
                        'torch==1.8.1',
                        ],
      python_requires='>=3.9',
      zip_safe=True)

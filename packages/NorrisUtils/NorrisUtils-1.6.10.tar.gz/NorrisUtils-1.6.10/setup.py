#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages
import os


def read_requirements():
    """Parse requirements from requirements.txt."""
    req_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    with open(req_path) as f:
        return f.read().splitlines()


setup(
    name='NorrisUtils',
    version='1.6.10',
    description=(
        'requirements'
    ),
    long_description=open('README.md').read(),
    author='AlaricNorris',
    author_email='norris.sly@gmail.com',
    maintainer='AlaricNorris',
    maintainer_email='norris.sly@gmail.com',
    license='BSD License',
    packages=find_packages(),
    platforms=["all"],
    url='https://www.baidu.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries'
    ],
    # install_requires=[
    #     'requests>=2.19.1',
    #     'imagekitio>=4.0.1',
    #     'bs4>=0.0.1',
    #     'selenium>=4.14.0',
    # ],
    install_requires=read_requirements(),
)

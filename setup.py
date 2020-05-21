#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# Created Date: Thursday, May 21st 2020, 6:39:22 pm
# Author: Charlene Leong charleneleong84@gmail.com
# Last Modified: Thursday, May 21st 2020, 7:09:19 pm
###


""" Setup for Creating SSO Config file

The setup script defines the modules required to build this app
"""

import setuptools

with open("README.md") as fp:
    long_description = fp.read()

requirements = [
    "boto3",
]

dev_requirements = [
    "autopep8",
    "pylint",
    "pytest",
    "pytest-dotenv",
    "pytest-cov"
]

setuptools.setup(
    name="sso-config",
    version="0.0.1",

    description="Creating SSO Config file",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="Charlene Leong",

    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),

    install_requires=requirements,
    extras_require={"dev": dev_requirements},

    python_requires=">=3.7.5",

    classifiers=[
        "Development Status :: Development",

        "Intended Audience :: Public",

        "Programming Language :: Python :: 3.7.5",

        "Topic :: Utilities",

        "Typing :: Typed",
    ],
)


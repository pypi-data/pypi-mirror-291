#!/usr/bin/env python
from setuptools import setup, find_packages

COMPANY_NAME="LOGYCA"
PACKAGE_NAME = "logyca-pagination"
VERSION = "0.1.2"

install_requires = ["pydantic>=2.0.3","sqlalchemy>=2.0.6"]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=f'An integration package created by the company {COMPANY_NAME} to according to a query created with sqlalchemy, paginate its result and return the information in lists of items with page numbers that can be used in frontend grids.',
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    license='MIT License',
    author='Jaime Andres Cardona Carrillo',
    author_email='jacardona@outlook.com',
    url='https://github.com/logyca/python-libraries/tree/main/logyca-pagination',
    keywords="pagination, serverless, backend, fastapi",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python",
        "Topic :: Database",
        "Topic :: Database :: Front-Ends",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development",
        "Typing :: Typed",
    ],
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=install_requires,
)

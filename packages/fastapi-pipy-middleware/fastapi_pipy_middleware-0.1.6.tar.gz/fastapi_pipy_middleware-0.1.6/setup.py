# setup.py

from setuptools import setup, find_packages

setup(
    name='fastapi-pipy-middleware',
    version='0.1.6',
    packages=find_packages(),
    install_requires=[
        'fastapi',
        'starlette'
    ],
    description='A FastAPI middleware example',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://pypi.org/manage/projects/fastapi-pipy-middleware',
)
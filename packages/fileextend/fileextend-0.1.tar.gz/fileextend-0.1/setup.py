from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='fileextend',
    version='0.1',
    description='File extends',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Krzysztof Żyłka',
    author_email='krzysztofzylka@yahoo.com',
    install_requires=[
        'pathlib'
    ],
    packages=find_packages()
)
from setuptools import setup, find_packages


with open('README.md', 'r') as readme:
    long_description = readme.read()

with open('requirements.txt') as requirements:
    required = requirements.read().splitlines()

setup(
    name="c3tl",
    version="0.0.1",
    author="e183b796621afbf902067460",
    author_email="606d18446a06fe9738fd@gmail.com",
    url="https://github.com/e183b796621afbf902067460/c3tl",
    packages=find_packages(),
    long_description=long_description,
    install_requires=required,
)
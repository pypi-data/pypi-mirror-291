from setuptools import setup, find_packages

setup(
    name="taiga-client",
    version="1.1.1",
    author="Alextanker",
    author_email="alextanker@kionclient.pro",
    description="A Python client for Taiga Rest API",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Alextanker/taiga-client",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "requests",
    ],
)
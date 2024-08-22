from setuptools import setup, find_packages

setup(
    name='laborit_heigen',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        "langchain",
        "langchain_core"
    ]

)
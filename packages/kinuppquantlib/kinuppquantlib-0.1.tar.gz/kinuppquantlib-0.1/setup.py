from setuptools import setup, find_packages

setup(
    name="kinuppquantlib",
    version="0.1",
    description="A quantitative library for stock market analysis.",
    packages=find_packages(include=["kinuppquantlib"]),
    author="Caio Kinupp",
    author_email="ckinupp@gmail.com",
    zip_safe=False,
)

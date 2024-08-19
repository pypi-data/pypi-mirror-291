"""
Setup file for pysonarr
"""

from setuptools import find_packages, setup

long_description = open("README.md").read()

setup(
    name="pysonarr",
    version="0.1.0",
    description="Python API wrapper for Sonarr API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Jacques-Murray/pysonarr",
    author="Jacques Murray",
    author_email="jacquesmmurray@gmail.com",
    packages=find_packages(),
    install_requires=[
        "requests",
        "pydantic",
        "python-dotenv"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.11"
)

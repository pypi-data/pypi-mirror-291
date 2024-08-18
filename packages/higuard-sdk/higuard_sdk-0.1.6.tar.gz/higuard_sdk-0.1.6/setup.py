# setup.py
from setuptools import setup, find_packages


def parse_requirements(filename):
    with open(filename) as f:
        return [line.strip() for line in f if line and not line.startswith("#")]


setup(
    name="higuard_sdk",
    version="0.1.6",
    author="Derek Li",
    author_email="derekli11204@gmail.com",
    description="Python SDK for Error Dashboard",
    url="https://github.com/HiQ-Apps/error_dashboard_python",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=parse_requirements("requirements.txt"),
)

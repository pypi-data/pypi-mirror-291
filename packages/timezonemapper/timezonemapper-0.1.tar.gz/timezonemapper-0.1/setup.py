from setuptools import setup, find_packages

setup(
    name="timezonemapper",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pytz",
    ],
    description="A Python library to map descriptive time zone names to their respective time zone identifiers.",
    author="Siddharth Rohit Jain",
    author_email="tellsiddh@gmail.com",
    url="https://github.com/tellsiddh/timezonemapper",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

from setuptools import setup

with open ("README.md", "r") as f:
    description = f. read ()

setup(
    name="realscreenPy",
    version="1.0.1",
    long_description=description,
    long_description_content_type= "text/markdown",
)
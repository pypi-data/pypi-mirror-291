from setuptools import setup, find_packages
import os

# Read the contents of your README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name="finceptapi",
    version="0.1.2",
    description="A Python client library for Fincept API",
    author="Fincept Corporation",
    author_email="support@fihcept.in",
    url="https://github.com/Fincept-Corporation/finceptapi",
    long_description=long_description,  # This is where you include your README content
    long_description_content_type="text/markdown",  # Ensure this is set correctly
    packages=find_packages(),
    install_requires=[
        "requests",
        "python-dotenv",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)

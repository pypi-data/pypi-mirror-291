from setuptools import setup, find_packages

setup(
    name="finceptapi",
    version="0.1.0",
    description="A Python client library for Fincept API",
    author="Fincept Corporation",
    author_email="support@fihcept.in",
    url="https://github.com/Fincept-Corporation/finceptapi",
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

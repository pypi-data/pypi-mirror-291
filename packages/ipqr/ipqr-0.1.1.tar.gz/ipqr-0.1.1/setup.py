from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ipqr",
    version="0.1.1",
    author="Kasun Dulara",
    author_email="kasundularaam@gmail.com",
    description="A CLI tool to generate QR codes for local server URLs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kasundularaam/ipqr",
    packages=find_packages(),
    install_requires=[
        "qrcode",
        "netifaces",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        "console_scripts": [
            "ipqr=ipqr.ipqr:run",
        ],
    },
)

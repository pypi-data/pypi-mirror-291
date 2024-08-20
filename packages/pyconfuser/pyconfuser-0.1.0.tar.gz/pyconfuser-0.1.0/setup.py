from setuptools import setup, find_packages

setup(
    name="pyconfuser",
    version="0.1.0",
    author="MichaelXF",
    author_email="michaelxfr@gmail.com",
    description="A Python obfuscation tool.",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)

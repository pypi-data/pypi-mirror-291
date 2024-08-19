from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="kisho",
    version="0.3.0",
    packages=find_packages(),
    install_requires=[
        "openai",
        "requests",
        "fastapi",
        "uvicorn",
        "networkx",
        "matplotlib",
    ],
    author="Aryan Jain",
    author_email="aryan@kisho.app",
    description="A tracing library for OpenAI API calls and custom functions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kisholabs/obs-v2",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.7",
)

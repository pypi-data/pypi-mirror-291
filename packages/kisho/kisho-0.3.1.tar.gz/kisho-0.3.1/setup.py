from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="kisho",
    version="0.3.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
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
    url="https://github.com/kisholabs/sdk-v3",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
)
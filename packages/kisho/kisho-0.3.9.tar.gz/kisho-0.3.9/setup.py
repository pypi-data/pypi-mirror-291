from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="kisho",
    version="0.3.9",
    packages=find_packages(),
    install_requires=[
        "openai>=0.27.0",
        "requests>=2.25.0",
        "fastapi>=0.68.0",
        "uvicorn>=0.15.0",
        "networkx>=2.5",
        "matplotlib>=3.3.0",
        "python-dotenv>=0.19.0",
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
    ],
    python_requires=">=3.7",
)
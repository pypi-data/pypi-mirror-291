from setuptools import setup, find_packages

setup(
    name="WrappedLLM",
    version="0.1.4",
    packages=find_packages(),
    install_requires=[
        "openai",
        "anthropic",
        "google-generativeai",
        "pydantic",
    ],
    author="Jayam Gupta",
    author_email="guptajayam47@gmail.com",
    description="A wrapper for various large language models including GPT, Claude, and Gemini",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/llm-wrapper",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
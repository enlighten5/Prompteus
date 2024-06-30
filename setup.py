from setuptools import setup, find_packages

setup(
    name="Prompteus",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "langchain",
        "openai",
    ],
    author="enlighten5",
    author_email="enlighten5.github@gmail.com",
    description="A library of decorators for LLM interactions and agent graphs",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/enlighten5/prompteus",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
from setuptools import setup, find_packages

setup(
    name="test0707",
    version="0.1.0",
    author="Shaxboz",
    author_email="shoxa0212@gmail.com",
    description="Convert any number to words in Uzbek",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/shoxa0707/num2word-uz",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)

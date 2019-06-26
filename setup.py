import setuptools

with open("README.md", "r") as readme:
    long_description = readme.read()

setuptools.setup(
    name="pysplunk",
    version="0.0.2",
    author="Alisson Prado da Cruz",
    author_email="alissonpdc@gmail.com",
    description="A simple and complete package to abstract main operations with Splunk API (send data / run search / get result)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alissonpdc/pysplunk",
    packages=setuptools.find_packages(),
    keywords=['splunk'],
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="datatrail",
    version="0.0.10",
    author="Jiun Yang Yen",
    author_email="withinfinitelife@gmail.com",
    description="A data processing logger for data analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/qks1lver/datatrail",
    python_requires='>=3.5.0',
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ),
)

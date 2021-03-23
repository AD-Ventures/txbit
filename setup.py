import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="txbit",
    version="0.0.1",
    author="AD Ventures",
    author_email="abir.dahlin.ventures@gmail.com",
    description="A Python wrapper for the Txbit API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AD-Ventures/txbit",
    packages=setuptools.find_packages(),
    install_requires=['requests'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.3',
)

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytesting",
    version="0.1.0",
    author="Griffin Austin",
    author_email="griffinaustin@protonmail.com",
    description="A simple and efficient Python3 test framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GriffinAustin/pytesting",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux"
    ],
    python_requires='>=3.0',
    test_suite="test_all",
)

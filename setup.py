from setuptools import setup, find_packages

setup(
    name = "boolevard",
    version = "0.1.0",
    description = "BooLEVARD: Boolean Logical Evaluation of Activation and Represion in Directed pathways",
    author = "Marco Fariñas Fernandez",
    author_email = "marco.farinas@gmail.com",
    long_description = open("README.md").read(),
    long_description_content_type = "text/markdown",
    url = "https://github.com/farinasm/boolevard",
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages = find_packages(),
    install_requires = [
        "pyeda==0.26.0",
        "mpbn",
        "colomoto_jupyter",
        "pandas"
    ]
)

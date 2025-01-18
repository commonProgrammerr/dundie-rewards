import os
from setuptools import setup, find_packages


def read(*paths):
    """Reads the content of a text file safely.
    >>> read("dundie", VERSION)
    '0.1.0'
    >>> read("README.md")
    ...
    """
    root_path = os.path.dirname(__file__)
    filepath = os.path.join(root_path, *paths)
    with open(filepath) as file_:
        return file_.read().strip()


def read_requirements(path):
    """Return a list of requirements from a text file"""
    return [
        line.strip()
        for line in read(path).split("\n")
        if not line.startswith(("#", "git+", '"', "-"))
    ]


setup(
    name="dundie",
    version="0.1.0",
    packages=find_packages(exclude=["integration/*"]),
    include_package_data=True,
    author="André Escorel",
    author_email="gustavo.escorel@gmail.com",
    description="Reward point system for Dunder Mifflin",
    url="https://github.com/commanProgrammerr/dundie-rewards",
    python_requires=">=3.10",
    entry_points={"console_scripts": ["dundie=dundie.__main__:main"]},
    install_requires=read_requirements("requirements.txt"),
    extras_require={
        "dev": read_requirements("requirements.dev.txt"),
        "test": read_requirements("requirements.test.txt"),
    },
)

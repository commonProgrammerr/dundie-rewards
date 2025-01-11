from setuptools import setup, find_packages

setup(
    name="dundie",
    version="0.1.0",
    packages=find_packages(),
    author="André Escorel",
    author_email="gustavo.escorel@gmail.com",
    description="Reward point system for Dunder Mifflin",
    url="https://github.com/commanProgrammerr/dundie-rewards",
    python_requires=">=3.10",
    entry_points={"console_scripts": ["dundie=dundie.__main__:main"]},
)

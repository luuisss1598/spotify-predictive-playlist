from setuptools import setup, find_packages

setup(
    name="custom_packages",
    version="0.1",
    description="Import custom packages to create a more structured project for ETL/ELT under ./src",
    author="luuisss1598",
    packages=find_packages("src"),
    package_dir={"": "src"},
)
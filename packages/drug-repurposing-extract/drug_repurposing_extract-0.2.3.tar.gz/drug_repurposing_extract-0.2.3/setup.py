from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='drug_repurposing_extract',
    packages=find_packages(include=["drug_repurposing"]),
    version='0.2.3',
    description='Library for automatic generation of drug repurposing data',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Shiva Aryal',
    include_package_data=True,
    package_data={'': ['rf_model.pkl']}
)
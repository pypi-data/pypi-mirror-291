from setuptools import setup,find_packages

with open("README.md","r") as f:
    description=f.read()

setup(
    name="StefanTools",
    version="1.1.1",
    packages=find_packages(),
    install_requires=[
        "rich",
        "inputimeout"
    ],
    long_description=description,
    long_description_content_type="text/markdown"
)
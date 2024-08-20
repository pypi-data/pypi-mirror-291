from setuptools import setup, find_packages

setup(
    name="prova_badiello",
    version="1.1.0",
    description="A simple package that prints Hello World",
    author="Il tuo nome",
    author_email="marco.baddy04@gmial.com",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

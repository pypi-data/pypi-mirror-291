from setuptools import setup, find_packages

import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='mahul-openai-utils',
    version='0.1.2',
    long_description=README,
    long_description_content_type="text/markdown",
    author='Mahul Rana',
    author_email='mahulrana007@gmail.com',
    packages=find_packages(),
    install_requires=['openai'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)

from setuptools import setup, find_packages

setup(
    name='mahul-openai-utils',
    version='0.1.0',
    description='A reusable utility module for OpenAI API',
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

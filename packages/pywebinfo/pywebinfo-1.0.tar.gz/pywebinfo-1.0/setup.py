from setuptools import setup, find_packages

VERSION = '1.0'
DESCRIPTION = 'A Python package to simply extract metadata (title, description, image, favicon) of a webpage'

setup(
    name='pywebinfo',
    version=VERSION,
    description=DESCRIPTION,
    author='Kaustubh Prabhu',
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4'
    ],
    keywords=['python', 'webpage', 'website', 'metadata'],
)
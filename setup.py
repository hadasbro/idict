from io import open
from setuptools import setup

setup(
    name='Idict',
    version='1.0.1-SNAPSHOT',
    author='Slawomir Hadas',
    author_email='slawomir.hadas@yahoo.com',
    packages=['idict'],
    package_data={
        'idict': [],
    },
    install_requires=[],
    python_requires='>=2.6',
    description='Extended default dict with settable placeholder for default values',
    long_description=open('README.md', encoding='utf-8').readlines()[2],
    keywords=['dict', 'defaultdict', 'python'],
    homepage='https://github.com/hadasbro/idict',
)

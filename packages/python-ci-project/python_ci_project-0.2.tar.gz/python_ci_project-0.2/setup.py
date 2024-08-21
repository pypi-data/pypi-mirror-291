# setup.py

from setuptools import setup, find_packages

setup(
    name='python-ci-project',
    version='0.2',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'main=main:main',
        ],
    },
)

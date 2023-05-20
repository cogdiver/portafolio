from setuptools import setup

setup(
    name='wordcount',
    version='0.1',
    install_requires=[
        'apache-beam[gcp]==2.32.0',
    ],
)

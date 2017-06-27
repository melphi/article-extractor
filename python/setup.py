from os import path
from setuptools import setup


CURRENT_PATH = path.dirname(path.abspath(__file__))

with open(CURRENT_PATH + '/requirements.txt', 'r') as file:
    REQUIREMENTS = file.read().splitlines()

setup(
    name='crawler',
    version='0.0.1',
    description='Crawler',
    test_suite='tests',
    packages=['app'],
    include_package_data=True,
    zip_safe=False,
    install_requires=REQUIREMENTS)

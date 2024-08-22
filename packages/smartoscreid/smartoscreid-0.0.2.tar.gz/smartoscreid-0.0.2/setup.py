import numpy as np
import setuptools
import os.path as osp
from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r') as f:
        content = f.read()
    return content


def get_requirements(filename='requirements.txt'):
    here = osp.dirname(osp.realpath(__file__))
    with open(osp.join(here, filename), 'r') as f:
        requires = [line.replace('\n', '') for line in f.readlines()]
    return requires


def find_version():
    version_file = 'smartoscreid/__init__.py'
    with open(version_file, 'r') as f:
        exec(compile(f.read(), version_file, 'exec'))
    return locals()['__version__']


setup(
    name='smartoscreid',
    version=find_version(),
    description='People counting project',
    author='CLOUD Team',
    license='MIT',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://git02.smartosc.com/division-1/computer-vision-project/people_counting',
    packages=find_packages(),
    install_requires=get_requirements(),
    keywords=['Person Re-Identification', 'Deep Learning', 'Computer Vision']
)
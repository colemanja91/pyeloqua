from setuptools import setup, find_packages

import pyeloqua

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='pyeloqua',
    version=pyeloqua.__version__,
    description='Python wrapper functions for Eloqua APIs',
    long_description=readme(),
    url='https://github.com/colemanja91/pyeloqua',
    author='Jeremiah Coleman',
    author_email='colemanja91@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'requests',
        'pbr',
        'six'
    ],
    zip_safe=False,
    keywords = 'eloqua marketing automation api bulk'
)

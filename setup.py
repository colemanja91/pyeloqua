from setuptools import setup

import pyeloqua

setup(
    name='pyeloqua',
    version=pyeloqua.__version__,
    description='Python wrapper functions for Eloqua APIs',
    url='https://github.com/colemanja91/pyeloqua',
    author='Jeremiah Coleman',
    author_email='colemanja91@gmail.com',
    license='MIT',
    packages=['pyeloqua'],
    zip_safe=False
)

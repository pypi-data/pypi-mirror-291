# setup.py

from setuptools import setup, find_packages

setup(
    name='varsync',
    version='1.16',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'varsync=varsync.cli:main',
        ],
    },
    install_requires=[
        'mysql-connector-python',
    ],
    author='Sriharan',
    author_email='sriharan2544@gmail.com',
    description='A Python package for managing variables with a MySQL backend.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Sriharan-S/varsync',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

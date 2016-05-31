# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

install_requires = [
    'requests',
    'nose',
    'coverage',
    'rednose',
    'nose-exclude',
    'watchdog'
]

scripts = [
    'opentsdb_importer/bin/flush_data'
]

setup(
    name='opentsdb_importer',
    version='0.0.1',
    description='opentsdb_importer',
    long_description=readme,
    author='Thada Wangthammang',
    author_email='mildronize@gmail.com',
    url='',
    license='MIT',
    install_requires=install_requires,
    packages=find_packages(exclude=('docs')),
    include_package_data=True,
    scripts=scripts
)

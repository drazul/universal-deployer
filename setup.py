# -*- coding: utf-8 -*-

import os
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


version = "0.0.1"


def read_file(filename):
    if os.path.exists(filename):
        with open(filename) as fd:
            return fd.read()
    return ''


class PyTest(TestCommand):
    user_options = [
        ('pytest-args=', 'a', "Arguments to pass to py.test"),
    ]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest  # NOQA
        errno = pytest.main(self.pytest_args or ['--cov-report=term-missing'])
        sys.exit(errno)


setup(
    name='udeploy',
    version=version,
    description="Transforms tests in documentation, and viceversa",
    long_description=read_file('README.rst'),
    cmdclass={'test': PyTest},
    classifiers=[
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        # 'Programming Language :: Python :: 2.7',
        # 'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        # 'Programming Language :: Python :: Implementation :: PyPy',
        # 'License :: OSI Approved :: MIT License',
        'Topic :: System :: Installation/Setup',
        'Operating System :: OS Independent',
    ],
    keywords=(
        'deployment automatic-deployment iis curator nssm'
        'windows-service chocolatey universal-deployment liquibase'
        ),
    author='Daniel',
    author_email='',
    url='https://github.com/drazul/universal-deployer',
    # license='MIT',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    extras_require={
    },
    install_requires=[
        'pyyaml',
        'jinja2',
    ],
    entry_points={
        'console_scripts': [
            'udeploy = udeploy.__main__:main',
        ],
    },
)

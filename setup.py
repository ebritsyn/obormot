#!/usr/bin/env python3

"""Setup script."""

from setuptools import setup, find_packages

# pckgs =

setup(
    name="obormot",
    version="0.0.0",
    author="Britsyn Eugene, Luzyanin Artemiy, Rassolov Sergey",
    author_email="ebritsyn@gmail.com, kek@obormor.com, kek@obormot.ru",
    url="https://github.com/ebritsyn/obormot",
    license="MIT",
    packages=find_packages(exclude=['tests*']),
    install_requires=[
        "python-telegram-bot",
        "keras",
        "pillow",
        "opencv-python",
        "tensorflow",
        "h5py",
        "numpy",
        "dlib",
    ],
    setup_requires=[
        "pytest-runner",
        "pytest-pylint",
        "pytest-pycodestyle",
        "pytest-pep257",
        "pytest-cov",
    ],
    tests_require=[
        "pytest",
        "pylint",
        "pycodestyle",
        "pep257",
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ]
)

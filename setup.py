#!/usr/bin/env python3

"""Setup script."""

from setuptools import setup, find_packages


setup(
    name="obormot",
    version="0.0.0",
    author="Britsyn Eugene, Luzyanin Artemiy, Rassolov Sergey",
    author_email="ebritsyn@gmail.com, kek@obormor.com, kek@obormot.ru",
    url="https://github.com/ebritsyn/obormot",
    license="MIT",
    packages=find_packages(exclude=['tests*']),
    install_requires=[
    ],
    setup_requires=[
        "pytest-runner",
        "pytest-pylint",
        "pytest-pycodestyle",
        "pytest-pep257",
        "pytest-cov",
        "dlib",
        "pillow",
        "h5py",
        "python-telegram-bot",
        "keras",
    ],
    tests_require=[
        "pytest",
        "pylint",
        "pycodestyle",
        "pep257",
    ],
    extras_require={
        "tf": ["tensorflow>=1.4.0"],
        "tf_gpu": ["tensorflow-gpu>=1.4.0"],
        "opencv-python": ["opencv-python"],
    },
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ]
)

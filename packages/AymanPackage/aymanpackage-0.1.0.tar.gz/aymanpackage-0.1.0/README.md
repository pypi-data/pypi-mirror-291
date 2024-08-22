# Developing Python Packages

## Project Description

this project is a template or a guide to help you develop your own python package.


## Project Structure
    .
    ├── python-package
    │   ├── pythonPackage
    │   │   ├── __init__.py
    │   │   ├── subpackage
    │   │   │   ├── __init__.py
    │   │   │   └── module.py
    │   ├── setup.py
    │   ├── README.md
    │   ├── HISTORY.md
    │   ├── LICENSE
    │   ├── requirements.txt
    │   ├── MANIFEST.in
    │   ├── tox.ini
    │   └── tests
    │       ├── __init__.py
    │       ├── pytest.ini
    │       ├── config.py
    │       └── test_sub_package
    │           ├── __init__.py
    │           └── test_module.py


## Installation

```bash

pip install -e .

```

## How to build distribution package

```bash
python setup.py sdist bdist_wheel
```
sdidt: source distribution

bdist_wheel: wheel distribution

## Upload package to PyPi

```bash
twine upload dist/*
```

## Upload package to TestPyPi

```bash
twine upload -r testpypi dist/*
```
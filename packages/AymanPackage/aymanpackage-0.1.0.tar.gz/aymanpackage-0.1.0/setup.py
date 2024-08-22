
from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.md') as history_file:
    history = history_file.read()

setup(
    name='AymanPackage',
    version='0.1.0',
    author='Ayman Elsayeed',
    description='A small example package',
    packages=find_packages(include=['python-package', 'python-package.*']),
    install_requires=['numpy', 'pandas', 'scikit-learn'],
    python_requires='>=3.6',
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
    ],
)
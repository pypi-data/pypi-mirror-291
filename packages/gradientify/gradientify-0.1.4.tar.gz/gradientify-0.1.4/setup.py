from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='gradientify',
    version='0.1.4',
    author='knelly999',
    description='A Python package for gradient prints or inputs',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/knelly999/gradientify',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
)

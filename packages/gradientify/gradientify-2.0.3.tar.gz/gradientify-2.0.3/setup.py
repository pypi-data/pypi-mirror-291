from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='gradientify',
    version='2.0.3',
    author='virtual',
    description='A Python package for gradient prints or inputs',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://vanishnet.netlify.app/',
    packages=find_packages(),
    python_requires='>=3.11',
)

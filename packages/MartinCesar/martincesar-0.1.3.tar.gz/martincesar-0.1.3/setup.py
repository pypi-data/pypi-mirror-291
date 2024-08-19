from setuptools import setup, find_packages

setup(
    name='MartinCesar',
    version='0.1.3',    
    packages=find_packages(), 
    author='Martin',
    author_email='tu.email@example.com',
    description='Descripción de lo que hace tu librería',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    python_requires='>=3.6',
)

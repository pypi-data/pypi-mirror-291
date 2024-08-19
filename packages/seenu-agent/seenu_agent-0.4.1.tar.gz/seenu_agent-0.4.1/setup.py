from setuptools import setup,find_packages
import os

def read_file(filename):
    with open(os.path.join(os.path.dirname(__file__), filename), encoding='utf-8') as f:
        return f.read()

setup(
    name="seenu_agent",
    version="0.4.1",
    description='A Python package for creating and managing agents.',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    author='Seenuvasan T',
    author_email='seenuthiruvpm@gmail.com',
    packages=find_packages(),
    
)

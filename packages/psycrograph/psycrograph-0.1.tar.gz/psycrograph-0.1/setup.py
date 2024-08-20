from setuptools import setup, find_packages

setup(
    name='psycrograph',
    version='0.1',
    description='A toolkit for drawing psychrometric charts and evolutions',
    author_email='jose@azzamura.com',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.26.4',
        'matplotlib>=3.8.3',
        'scipy>=1.12.0'
    ],
)

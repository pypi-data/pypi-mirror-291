from setuptools import setup, find_packages

setup(
    name='Social_LIWC', 
    version='0.1',
    packages = find_packages(),
    install_requires = [
        #place depedencies here
        'pandas>=2.1.4',
        'fastapi>=0.112.1',
        'liwc>=0.5.0'
    ]
)


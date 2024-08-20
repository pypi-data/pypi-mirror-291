from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(name='AdaptFTIR',
    version='0.1.0',
    packages=find_packages(),
    url='https://github.com/Niklas-LK/AdaptFTIR',
    license='MIT',
    author='Niklas Leopold-Kerschbaumer',
    author_email='niklas.leopold-kerschbaumer@hotmail.com',
    description='Domain adaptation for FTIR spectra',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=['numpy', 'typing']

)
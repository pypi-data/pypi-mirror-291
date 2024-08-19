from setuptools import setup, find_packages
setup(
name='centigrad',
version='0.1.1',
author='Jose Cruzado',
author_email='josecruzado2103@gmail.com',
description='This is a simple package to train neural networks leveraging a Variable object that supports automatic differentiation',
url = "https://github.com/josecruzado21/centigrad",
packages=find_packages(),
classifiers=[
'Programming Language :: Python :: 3',
'License :: OSI Approved :: MIT License',
'Operating System :: OS Independent',
],
python_requires='>=3.6',
)
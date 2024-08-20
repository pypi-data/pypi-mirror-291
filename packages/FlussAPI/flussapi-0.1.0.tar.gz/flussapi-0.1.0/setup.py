from setuptools import setup, find_packages
setup(
name='FlussAPI',
version='0.1.0',
author='Njeru Ndegwa',
author_email='njeru@fluss.ip',
description='An API package for Home Assistant Plugin to operate a Fluss device',
packages=find_packages(),
classifiers=[
'Programming Language :: Python :: 3',
'License :: OSI Approved :: MIT License',
'Operating System :: OS Independent',
],
python_requires='>=3.6',
)
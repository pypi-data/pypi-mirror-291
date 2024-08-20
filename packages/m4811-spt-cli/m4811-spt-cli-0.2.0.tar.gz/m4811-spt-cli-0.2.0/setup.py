##############################################################################
# 
# Module: setup.py
#
# Description:
#     setup to install the test_proc_4811 package
#
# Author:
#     MCCI , MCCI   AUG 2024
#
##############################################################################

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of your README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='m4811-spt-cli',
    version='0.2.0',
    description='The model4811 mfg test script.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='MCCI Corporation',
    author_email='vinayn@mcci.com',
    url='https://gitlab-x.mcci.com/mcci/hardware/catena/mfg/test-proc-4811',
    packages=find_packages(),
    install_requires=[
        'modbus_tk',  # Add other dependencies if necessary
        'pyserial',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: zlib/libpng License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)


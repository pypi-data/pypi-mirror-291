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

setup(
    name='m4811-spt-cli',
    version='0.1.0',
    description='The model4811 mfg test script..',
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


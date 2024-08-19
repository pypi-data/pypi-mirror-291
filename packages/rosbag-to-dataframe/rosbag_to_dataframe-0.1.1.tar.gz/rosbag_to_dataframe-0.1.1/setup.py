# setup.py
"""
Setup script for the rosbag_to_dataframe package.

This script uses setuptools to package the rosbag_to_dataframe module,
which provides functionality to extract data from ROS2 bag files into pandas DataFrames.
"""

from setuptools import setup, find_packages

setup(
    name='rosbag_to_dataframe',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'rosbags'
    ],
    description='A package to extract data from ROS2 bag files into pandas DataFrames.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Abhay Chaudhary',
    url='https://github.com/Abhayindia/rosbag_to_dataframe',
)

# setup.py
"""
Setup script for the rosbag_to_dataframe package.

This script uses setuptools to package the rosbag_to_dataframe module,
which provides functionality to extract data from ROS2 bag files into pandas DataFrames.
"""

from setuptools import setup

setup(
    name='rosbag-to-dataframe',
    version='0.2.1',
    description='A package to extract data from ROS2 bag files into pandas DataFrames.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Abhay Chaudhary',
    packages=['rosbag_to_dataframe'],
    install_requires=[
        'pandas',
        'numpy',
        'rosbag2_py'
    ],
)


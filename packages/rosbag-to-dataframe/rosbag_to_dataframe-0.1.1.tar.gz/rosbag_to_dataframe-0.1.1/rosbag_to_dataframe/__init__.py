# rosbag_to_dataframe/__init__.py
"""
rosbag_to_dataframe

This package provides functionality to extract data from ROS1 and ROS2 bag files 
and convert it into pandas DataFrames for further analysis.
"""

from .extractor import extract_data_from_bag

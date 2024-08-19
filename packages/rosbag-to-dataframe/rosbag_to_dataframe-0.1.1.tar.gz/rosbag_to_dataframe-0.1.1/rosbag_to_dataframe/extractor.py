"""
Extractor module for converting ROS bag files into pandas DataFrames.

This module provides functions to extract data from ROS1 and ROS2 bag files
and convert them into pandas DataFrames for further analysis.
"""

import os
from pathlib import Path

import pandas as pd
from rosbags.highlevel import AnyReader


def get_dataframe(reader, topic, fields):
    """
    Extracts data from the specified topic in the ROS bag file and returns it as a DataFrame.

    Parameters:
        reader (AnyReader): Reader object for accessing the bag file.
        topic (str): The topic from which data is to be extracted.
        fields (list): The fields to extract from the message.

    Returns:
        pd.DataFrame: A DataFrame containing the extracted data.
    """
    data = []
    for connection, _, rawdata in reader.messages():
        if connection.topic == topic:
            try:
                msg = reader.deserialize(rawdata, connection.msgtype)
                if all(hasattr(msg, field) for field in fields):
                    row = [getattr(msg, field) for field in fields]
                    data.append(row)
                else:
                    missing_fields = [field for field in fields if not hasattr(msg, field)]
                    print(f"Warning: Missing fields {missing_fields} in message.")
            except (ValueError, AttributeError) as e:
                print(f"Error deserializing message: {e}")
                return pd.DataFrame()  # Return an empty DataFrame if an error occurs
    return pd.DataFrame(data, columns=fields)


def extract_data_from_bag(bag_files, topic, fields):
    """
    Extracts data from a list of bag files for a specified topic and fields.

    Parameters:
        bag_files (list): List of paths to the bag files.
        topic (str): The topic from which data is to be extracted.
        fields (list): The fields to extract from the message.

    Returns:
        pd.DataFrame: A DataFrame containing the combined extracted data from all bag files.
    """
    dataframes = []

    for bag_file in bag_files:
        if not os.path.exists(bag_file):
            print(f"Bag file not found: {bag_file}")
            continue

        try:
            with AnyReader([Path(bag_file)]) as reader:
                topics = {connection.topic for connection, _, _ in reader.messages()}
                if topic not in topics:
                    print(f"Topic '{topic}' not found in bag file: {bag_file}")
                    continue

                dataframe = get_dataframe(reader, topic, fields)
                if not dataframe.empty:
                    dataframes.append(dataframe)
                else:
                    print(f"No valid data extracted from bag file: {bag_file}")
        except (OSError, ValueError) as e:
            print(f"Error reading bag file {bag_file}: {e}")

    if dataframes:
        return pd.concat(dataframes, ignore_index=True)

    print("No dataframes to concatenate.")
    return pd.DataFrame()  # Return an empty DataFrame if no valid data

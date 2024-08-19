# rosbag_to_dataframe

[![Pylint](https://github.com/Abhayindia/rosbag_to_dataframe/actions/workflows/pylint.yml/badge.svg)](https://github.com/Abhayindia/rosbag_to_dataframe/actions/workflows/pylint.yml)

`rosbag_to_dataframe` is a Python package for extracting data from ROS1 and ROS2 bag files and converting it into pandas DataFrames. This package allows you to easily work with ROS bag file data for analysis and processing.

## Requirements
To use the rosbag_to_dataframe package, you need to have the following dependencies installed:
- `Python 3.7+:` Ensure you have Python 3.6 or later installed.
- `pandas:` For handling data frames.
- `rosbags:` For reading ROS bag files. Make sure you have the rosbags library installed, which supports both ROS1 and ROS2 formats.
You can install the required dependencies using pip:
~~~
pip install pandas rosbags
~~~

## Steps to install the package locally
1. Clone this repository or download the package files.
2. Navigate to the directory containing the setup.py file.
3. Run the following command:
~~~
pip install .
~~~

## Steps to use the package to extract data from ROS bag files:
1. Import the package:
~~~
from rosbag_to_dataframe import extract_data_from_bag
~~~
2. Specify the bag files, topic, and fields:
~~~
bag_files = ['/path/to/your/bagfile1.bag', '/path/to/your/bagfile2.bag']  # List of ROS bag files
topic = '/your_topic'  # Topic to extract data from
fields = ['field1', 'field2']  # List of fields to extract from the message
~~~
3. Extract data:
~~~
dataframe = extract_data_from_bag(bag_files, topic, fields)
~~~

## Error Handling
- `File Not Found:` If a specified bag file does not exist, a warning will be printed, and the file will be skipped.
- `Topic Not Found:` If the specified topic is not present in a bag file, a warning will be printed, and the file will be skipped.
- `Field Not Found:` If any specified fields are missing from the messages, a warning will be printed. The processing will continue, but missing fields will be noted.
- `Deserialization Errors:` If an error occurs during message deserialization, the affected file will be skipped, and an empty DataFrame will be returned for that file.

## Contributing
If you would like to contribute to this package, please fork the repository and submit a pull request with your changes. Make sure to include tests and documentation updates as needed.

## License
This package is licensed under the MIT License. See the LICENSE file for more details.

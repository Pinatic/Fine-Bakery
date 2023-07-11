Code in this directory is called from the main script and is a part of the trend prediction pipeline.

The `merge_and_inspect.py` file is responsible for data parsing, cleaning, plotting and analyzing. The parser clears out all the non-ASCII symbols and some punctuation marks from string data types, gets the numbers according to certain regular expressions out of the columns that are expected to be float or integer, and converts the columns to their predefined data types, which are specified in the metadata. The metadata represents a field in a configuration file structured as a list of pairs where the first value is a column name and the second one is a data type that the column should be converted to. It collects the statistics about the separate files and the final cleaned file such as the number of columns, rows, unique and missing values in each column. This module is called if the command flag -p (--parse) is set to True.

The `categorizer.py` file is responsible for categorizing the product claims. After cleaning out the measurement abbreviations (for example, kcal) and punctuation marks, the product claims found in the output file after the data preparation process are split into sentences, sorted in the descending order of their frequencies, and used as category names to group the matching claims. The top n categories of claims can be used for trend prediction. The claim categories are persisted in a file on a local machine. This module is called if the command flag -c (--categorize) is set to True.

The `data_selector.py` file is responsible for selecting the data matching one of the most popular product claims. Selected data is stored in a file and persisted on a local machine. This module is called every time the trend prediction pipeline is run - this is a mandatory step.

The `XML_parser.py` file represents the object that reads and parses the raw data, merges and collects the statistics of the cleaned data. It is used in a `merge_and_inspect.py` file to work with the raw data.

All files in this directory are written by Anna Sorova. If there are any questions you can contact me at anyabalerina@gmail.com.

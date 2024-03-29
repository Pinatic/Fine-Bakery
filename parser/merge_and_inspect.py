"""In this module all the files with the raw data are read, preprocessed according to the configuration file and
metadata containing the predefined column types and merged it into one csv file

By: Anna Sorova
"""

from functools import reduce
import pathlib
import yaml
import re
import string
import os
from parser.XML_parser import XML_Stats
import pandas as pd


def get_config(config_file):
    """
    Read config file

    Args:
        config_file (str): path to the config file

    Returns:
        config (any): returns configuration file
    """
    with open(config_file, 'r') as stream:
        config = yaml.safe_load(stream)
    return config


def read_xml_objects(file_dir, file_names):
    """
    Read the raw data files and create XML_Stats object from them

    Args:
        file_dir (str): directory name with the raw data files
        file_names (list): raw data files names

    Returns:
        l (list): returns list of the XML_Stats objects
    """
    return [XML_Stats([os.path.join(file_dir, file_name)]) for file_name in file_names]


def write_statistics_to_file(xmlstats_obj, dir_to, file_path=''):
    """
    Write the XML_Stats object statistics to the txt file

    Args:
        xmlstats_obj (XML_Stats): XML_Stats object
        dir_to (str): directory to write the XML_Stats object
        file_path (list): file name to write the XML_Stats object
    """
    if file_path == '':
        file_path = os.path.join(dir_to, pathlib.PurePath(xmlstats_obj.file_paths[0]).name + '.txt')
    else:
        file_path = os.path.join(dir_to, file_path)
    print('print statistics to txt file:', file_path)

    with open(file_path, 'w') as f:
        f.write('\nCommon info:\n' + str(xmlstats_obj) + '\n')
        f.write(
            '\nNumber of unique values per column (uniques values are shown if their amount is less than 12)\n' + xmlstats_obj.get_unique_values_stats())
        f.write('\nNumber of non nan values per column\n' + xmlstats_obj.get_not_nan_values_stats())


def write_possible_merging_problems(problems, dir_to):
    """
    Write problems which may be encountered while merging several XML_Stats objects

    Args:
        problems (list): list of problems which may be encountered while merging several XML_Stats objects
        dir_to (str): directory to write the possible problems

    Returns:
        file_path (str): file path where the possible problems were written to
    """
    file_path = os.path.join(dir_to, 'merge_problems.txt')
    print('print merging problems to txt file:', file_path)
    with open(file_path, 'w') as f:
        for line in problems:
            f.write('\n' + line[0] + '\n')
    return file_path


def merge_xmlstats_objs(xmlstats_objs):
    """
    Merge two XML_Stats objects into one XML_Stats object

    Args:
        xmlstats_objs (list): list of XML_Stats objects

    Returns:
         (XML_Stats): return two merged XML_Stats objects
    """
    return reduce(lambda obj1, obj2: obj1.merge_xmlstats_objects(obj2), xmlstats_objs)


def split_to_list(row):
    """
    Replace punctuation mark

    Args:
        row (str): row in the dataframe

    Returns:
        (str): resulting string with the replaced punctuations
    """
    return row.replace(';', ',')


def check_flavor_column(obj):
    """
    Preprocess Flavor column

    Args:
        obj (XML_Stats): instance of XML_Stats to work with
    """
    column_name = 'Flavor'
    obj.df[column_name] = obj.df[column_name].fillna('')
    obj.df[column_name] = obj.df[column_name].apply(lambda row: split_to_list(str(row)))
    obj.df[column_name] = obj.df[column_name].astype('string')


def clean_string(row):
    """
    Clean string from the punctuation marks using regular expression

    Args:
        row (str): row in the dataframe

    Returns:
        row (str): row matching regular expression
    """
    row = ''.join(filter(lambda x: x in string.printable, row))
    row = re.sub('[\s+`+*+\r+\n+\\\\+~|^$]', ' ', row)
    row = row.replace('\\r', ' ')
    row = row.replace('\\n', ' ')
    return row


def clean_string_columns(obj, column_name):
    """
    Preprocess any string columns in a dataframe

    Args:
        obj (XML_Stats): instance of XML_Stats to work with
        column_name: the string column name to be preprocessed
    """
    p = re.compile('[\w\s\-&.,/!:;+?_\'%\\(){}\"<>=\[\]]*')
    obj.df[column_name] = obj.df[column_name].fillna('')
    obj.df[column_name] = obj.df[column_name].apply(lambda row: clean_string(str(row)))
    for val in list(obj.df[column_name]):
        if not p.fullmatch(val):
            raise Exception('Following structure does not meet predifined metadata: ', val, ' in column ', column_name)
    obj.df[column_name] = obj.df[column_name].astype('string')


def clean_float64(row, p):
    """
    Get the number out of value in the dataframe

    Args:
        row (any): value in the dataframe

    Returns:
        row (int): return the float value found in the raw value or 0.0 if the number was not found
    """
    res = p.findall(str(row))
    if len(res) > 0:
        return res[0]
    return row


def clean_float64_columns(obj, column_name):
    """
    Preprocess any float64 columns in a dataframe

    Args:
        obj (XML_Stats): instance of XML_Stats to work with
        column_name: the float64 column name to be preprocessed
    """
    p = re.compile(r"[-+]?(?:\d*\.*\d+)")
    obj.df[column_name] = obj.df[column_name].apply(lambda row: clean_float64(row, p))
    obj.df[column_name] = pd.to_numeric(obj.df[column_name])


def clean_int64(row):
    """
    Get the number out of value in the dataframe

    Args:
        row (any): value in the dataframe

    Results:
        row (int): return the integer value found in the raw row or 0 if the number was not found
    """
    res = re.findall(r'\d+', str(row))
    if len(res) > 0:
        return res[0]
    return row


def clean_int64_columns(obj, column_name):
    """
    Preprocess any int64 columns in a dataframe

    Args:
        obj (XML_Stats): instance of XML_Stats to work with
        column_name: the int64 column name to be preprocessed
    """
    obj.df[column_name] = obj.df[column_name].apply(lambda row: clean_int64(row))
    obj.df[column_name] = obj.df[column_name].astype('int')


def clean_data(obj, metadata):
    """
    Preprocess dataframe columns according to the metadata containing predefined column types

    Args:
        obj (XML_Stats): instance of XML_Stats to work with
        metadata (dict): dictionary with the key representing the column name and the value representing the column type
    """
    for column, data_type in metadata.items():
        # in case the metadata field in config contains column names which don't exist
        if column in obj.df.columns:
            if data_type == 'string':
                clean_string_columns(obj, column)
            elif data_type == 'float64':
                clean_float64_columns(obj, column)
            else:
                clean_int64_columns(obj, column)


new_xmlstats_obj = None


def parse_and_clean(config_file):
    """
    Read, preprocess all the files with the raw data according to the configuration file and metadata containing
    the predefined column types and merge it into one csv file

    Args:
        config_file (string): path to the config file
    """
    config = get_config(config_file)
    file_dir = config['directory_from']
    file_names = config['file_paths']
    delete_columns = config['delete_columns']
    dir_to = config['directory_to']
    metadata = config['metadata']
    file_name_to = config['cleared_data_to']

    xmlstats_objs = read_xml_objects(file_dir, file_names)

    for obj in xmlstats_objs:
        obj.delete_columns(delete_columns)
        check_flavor_column(obj)
        clean_data(obj, metadata)
        write_statistics_to_file(obj, dir_to)

    problems_info = [xmlstats_objs[i].get_possible_merging_problems(xmlstats_objs[i + 1]) for i in
                     range(len(xmlstats_objs) - 1)]
    file_path = write_possible_merging_problems(problems_info, dir_to)
    for problem in problems_info:
        if not problem[1]:
            raise Exception('Check ' + file_path + ' file! Data sources can not be merged')

    # merge all files into one
    global new_xmlstats_obj
    new_xmlstats_obj = merge_xmlstats_objs(xmlstats_objs)
    write_statistics_to_file(new_xmlstats_obj, dir_to, file_path='cleared_merged_data_stats.txt')
    new_xmlstats_obj.categorize()
    new_xmlstats_obj.write_to_csv(dir_to, file_name_to)


if __name__ == "__main__":
    parse_and_clean("./../config.yaml")

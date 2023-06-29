# Created by asorova

from functools import reduce
import pathlib
import yaml
import re
import string
import os
from XML_parser import XML_Stats
import pandas as pd


def get_config():
    with open("./../config.yaml", 'r') as stream:
        config = yaml.safe_load(stream)
    return config


def read_xml_objects(file_dir, file_names):
    return [XML_Stats([os.path.join(file_dir, file_name)]) for file_name in file_names]


def write_statistics_to_file(xmlstats_obj, dir_to, file_path=''):
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
    file_path = os.path.join(dir_to, 'merge_problems.txt')
    print('print merging problems to txt file:', file_path)
    with open(file_path, 'w') as f:
        for line in problems:
            f.write('\n' + line[0] + '\n')
    return file_path


def merge_xmlstats_objs(xmlstats_objs):
    return reduce(lambda obj1, obj2: obj1.merge_xmlstats_objects(obj2), xmlstats_objs)


def split_to_list(row):
    return row.replace(';', ',')


def check_flavor_column(obj):
    column_name = 'Flavor'
    obj.df[column_name] = obj.df[column_name].fillna('')
    obj.df[column_name] = obj.df[column_name].apply(lambda row: split_to_list(str(row)))
    obj.df[column_name] = obj.df[column_name].astype('string')


def clean_string(row):
    row = ''.join(filter(lambda x: x in string.printable, row))
    row = re.sub('[\s+`+*+\r+\n+\\\\+~|^$]', ' ', row)
    row = row.replace('\\r', ' ')
    row = row.replace('\\n', ' ')
    return row


def clean_string_columns(obj, column_name):
    p = re.compile('[\w\s\-&.,/!:;+?_\'%\\(){}\"<>=\[\]]*')
    obj.df[column_name] = obj.df[column_name].fillna('')
    obj.df[column_name] = obj.df[column_name].apply(lambda row: clean_string(str(row)))
    for val in list(obj.df[column_name]):
        if not p.fullmatch(val):
            raise Exception('Following structure does not meet predifined metadata: ', val, ' in column ', column_name)
    obj.df[column_name] = obj.df[column_name].astype('string')


def clean_float64(row, p):
    res = p.findall(str(row))
    if len(res) > 0:
        return res[0]
    # if the value was nan we return nan, not 0.0 (interpolation may be needed)
    return row


#     return 0.0

def clean_float64_columns(obj, column_name):
    p = re.compile(r"[-+]?(?:\d*\.*\d+)")
    obj.df[column_name] = obj.df[column_name].apply(lambda row: clean_float64(row, p))
    obj.df[column_name] = pd.to_numeric(obj.df[column_name])


def clean_int64(row):
    res = re.findall(r'\d+', str(row))
    if len(res) > 0:
        return res[0]
    # if the value was nan we return nan, not 0 (interpolation may be needed)
    return row


def clean_int64_columns(obj, column_name):
    obj.df[column_name] = obj.df[column_name].apply(lambda row: clean_int64(row))
    obj.df[column_name] = obj.df[column_name].astype('int')


def clean_data(obj, metadata):
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


def main():
    config = get_config()
    file_dir = config['directory_from']
    file_names = config['file_paths']
    delete_columns = config['delete_columns']
    dir_to = config['directory_to']
    metadata = config['metadata']
    file_name_to = config['cleared_data_to']

    # read all files
    xmlstats_objs = read_xml_objects(file_dir, file_names)

    # clear
    for obj in xmlstats_objs:
        #         obj.delete_0_value_columns()
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
    main()

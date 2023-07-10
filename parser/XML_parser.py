"""
In this module the XML_Stats class is defined.
This class is used to work with the raw IMCD data and gather the statistics.

By: Anna Sorova
"""

import pandas as pd
import os
import numpy as np
from parser import categorizer


class XML_Stats():
    """
    Represents the object that reads and parses the raw data, merges and collects the statistics of the cleaned data.
    """
    _counter = 0

    def __init__(self, file_paths, df=None):
        """
        Args:
            counter (int): Counts the number of raw data files
            file_paths (list): Contains the file paths to all raw data files of this object
            df (csv file): dataframe of this object
        """
        XML_Stats._counter += 1
        self.id = XML_Stats._counter

        self.file_paths = file_paths
        if len(file_paths) == 1:
            self.df = self.read_data()
        else:
            if df is None:
                raise Exception('dataframe of XML_Stats can not be None!')
            self.df = df

    def read_data(self):
        """
        Parses all the sheets in excel file.

        Returns:
             data (dataframe): a dataframe containing raw data read from the file
        """
        res = pd.read_excel(self.file_paths[0], sheet_name=None)
        key = list(res.keys())[0]
        data = res[key][res[key]['Region'] == 'Not stated']
        for key in res:
            data = pd.concat([data, res[key]])
        return data

    def get_columns_amount(self):
        """
        Gets columns number.

        Returns:
             n (int): number of columns
        """
        return len(self.get_columns())

    def get_columns(self):
        """
        Gets columns.

        Returns:
            l (list): list of columns' names
        """
        return self.df.columns.values.tolist()

    def get_lines_amount(self):
        """
        Gets rows number.

        Returns:
            n (int): number of rows
        """
        return dict(self.df.count())['S.No.']

    def write_to_csv(self, dir_to, file_name):
        """
        Writes resulting data to csv file.

        Args:
            dir_to (str): directory to write to
            file_name(str): file to write to
        """
        file_path = os.path.join(dir_to, file_name)
        self.df.to_csv(file_path, encoding='utf-8', index=False)

    def categorize(self):
        """
        Cleans claims column so that it can be saved to the final file
        """
        self.df = categorizer.clean_data(self.df)

    def get_dataframe(self):
        """
        Gets dataframe of the object.

        Returns:
            df (dataframe): returns dataframe of the object
        """
        return self.df

    def are_mergable(self, xmlstats_obj):
        """
        Checks if two instances of this class can be merged.

        Args:
            xmlstats_obj (XML_Stats) - another instance of this class

        Returns:
            b (bool): returns bool value answering if two instances can be merged
        """
        col1 = self.get_columns()
        col2 = xmlstats_obj.get_columns()
        for c in col1:
            if c not in col2 or self.df[c].dtype != xmlstats_obj.df[c].dtype:
                return False
        return True

    def get_possible_merging_problems(self, xmlstats_obj):
        """
        Checks if two instances of this class can be merged.

        Args:
            xmlstats_obj (XML_Stats) - another instance of this class

        Returns:
            str_res (str): returns a string with the errors encountered by merging two objects
            b (bool): returns bool value answering if two instances can be merged
        """
        str_res = self.file_paths[0] + ' +\n' + xmlstats_obj.file_paths[0] + '\n'
        col1 = self.get_columns()
        col2 = xmlstats_obj.get_columns()
        errors = 0
        for c in col1:
            if c not in col2 or self.df[c].dtype != xmlstats_obj.df[c].dtype:
                errors += 1
                if c not in col2:
                    str_res += 'problem: column ' + c + ' does not exist\n'
                else:
                    str_res += 'problem: columns with the same name ' + c + f' have different types: {self.df[c].dtype}, {xmlstats_obj.df[c].dtype}\n'
        if errors == 0:
            str_res += 'Can be merged!\n'
        return (str_res, errors == 0)

    def merge_xmlstats_objects(self, xmlstats_obj):
        """
        Merge two instances of this class.

        Args:
            xmlstats_obj (XML_Stats) - another instance of this class

        Returns:
            xmlstats_obj (XML_Stats): returns the result of two merged instnaces of this class
        """
        if not self.are_mergable(xmlstats_obj):
            raise Exception('Can not merge xmlstats objects!')
        combined_file_paths = self.file_paths + xmlstats_obj.file_paths
        data = pd.concat([self.df, xmlstats_obj.df])
        data = data.drop_duplicates(subset="Product Id")
        return XML_Stats(combined_file_paths, df=data)

    def count_values_in_columns(self):
        """
        Merge two instances of this class.

        Returns:
            l (list): returns the list of pairs where the first value is the column name, the second value is
        the number of not nan values in this column
        """
        value_counts = dict(self.df.replace('', np.nan).count())
        return [(name, value_counts[name]) for name in (sorted(value_counts, key=value_counts.get, reverse=True))]

    def delete_0_value_columns(self):
        """
        Deletes the columns with 0 non nan values (empty columns)
        """
        res = self.count_values_in_columns()
        need_to_delete = []
        for column in reversed(res):
            name, value = column[0], column[1]
            if value != 0:
                break
            need_to_delete.append(name)
        self.delete_columns(need_to_delete)

    # column_names - list of columns names which need to be deleted
    def delete_columns(self, column_names):
        """
        Deletes the columns passed to the function

        Args:
            column_names (list) - list of column names which should be deleted from the dataframe
        """
        self.df = self.df.drop(columns=column_names, axis=1, errors='ignore')

    def get_unique_values(self):
        """
        Counts unique values per column

        Returns:
            l (list) - returns the list of pairs where the first value is the column name, the second value is
        the number of unique values in this column
        """
        res = {}
        for c in self.get_columns():
            uniques = self.df[c].unique().tolist()
            res[c] = (len(uniques), uniques)
        return [(name, res[name]) for name in (sorted(res, key=lambda a: res[a][0], reverse=True))]

    def get_unique_values_stats(self):
        """
        Gets the unique values per column and turns this info into string

        Returns:
            str_res (str) - contains the information about the unique values per column
        """
        str_res = ''
        uniques = self.get_unique_values()
        for u, val in uniques:
            if len(val[1]) > 12:
                str_res += f'{(u, val[0])}\n'
            else:
                str_res += f'{(u, val[0], val[1])}\n'
        return str_res

    def get_not_nan_values_stats(self):
        """
        Gets the non nan values per column and turns this info into string

        Returns:
            str_res (str) - contains the information about the non nan values per column
        """
        str_res = ''
        non_nan_values = self.count_values_in_columns()
        ids = str(self.get_lines_amount())
        for u, val in non_nan_values:
            second_param = str(val) + '/' + ids
            str_res += f'{(u, second_param)}\n'
        return str_res

    def __str__(self):
        """
        Return the statistics about the object in a string format

        Returns:
            s (str) - return the statistics about the object in a string format
        """
        return f'file paths: {self.file_paths}, \nnumber of columns: {self.get_columns_amount()}, \nnumber of lines: {self.get_lines_amount()}'


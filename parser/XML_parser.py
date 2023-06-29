# Created by asorova

import pandas as pd
import os
import numpy as np


class XML_Stats():
    _counter = 0

    # file_paths contains one elem - original location or several elements - blending of several data sources
    def __init__(self, file_paths, df=None):
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
        # parse all the sheets in excel file
        res = pd.read_excel(self.file_paths[0], sheet_name=None)
        key = list(res.keys())[0]
        data = res[key][res[key]['Region'] == 'Not stated']
        for key in res:
            data = pd.concat([data, res[key]])
        return data

    def get_columns_amount(self):
        return len(self.get_columns())

    def get_columns(self):
        return self.df.columns.values.tolist()

    def get_lines_amount(self):
        return dict(self.df.count())['S.No.']

    def write_to_csv(self, dir_to, file_name):
        file_path = os.path.join(dir_to, file_name)
        self.df.to_csv(file_path, encoding='utf-8', index=False)

    def get_dataframe(self):
        return self.df

    def are_mergable(self, xmlstats_obj):
        col1 = self.get_columns()
        col2 = xmlstats_obj.get_columns()
        for c in col1:
            if c not in col2 or self.df[c].dtype != xmlstats_obj.df[c].dtype:
                return False
        return True

    def get_possible_merging_problems(self, xmlstats_obj):
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
        if not self.are_mergable(xmlstats_obj):
            raise Exception('Can not merge xmlstats objects!')
        combined_file_paths = self.file_paths + xmlstats_obj.file_paths
        data = pd.concat([self.df, xmlstats_obj.df])
        data = data.drop_duplicates(subset="Product Id")
        return XML_Stats(combined_file_paths, df=data)

    def count_values_in_columns(self):
        #         value_counts = dict(self.df.count())
        value_counts = dict(self.df.replace('', np.nan).count())

        return [(name, value_counts[name]) for name in (sorted(value_counts, key=value_counts.get, reverse=True))]

    def delete_0_value_columns(self):
        """
        let's delete columns with 0 values ('US Price/Litre', '0/5117')
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
        self.df = self.df.drop(columns=column_names, axis=1, errors='ignore')

    def get_unique_values(self):
        res = {}
        for c in self.get_columns():
            uniques = self.df[c].unique().tolist()
            res[c] = (len(uniques), uniques)
        return [(name, res[name]) for name in (sorted(res, key=lambda a: res[a][0], reverse=True))]

    def get_unique_values_stats(self):
        str_res = ''
        uniques = self.get_unique_values()
        for u, val in uniques:
            if len(val[1]) > 12:
                str_res += f'{(u, val[0])}\n'
            else:
                str_res += f'{(u, val[0], val[1])}\n'
        return str_res

    def get_not_nan_values_stats(self):
        str_res = ''
        non_nan_values = self.count_values_in_columns()
        ids = str(self.get_lines_amount())
        for u, val in non_nan_values:
            second_param = str(val) + '/' + ids
            str_res += f'{(u, second_param)}\n'
        return str_res

    def __str__(self):
        return f'file paths: {self.file_paths}, \nnumber of columns: {self.get_columns_amount()}, \nnumber of lines: {self.get_lines_amount()}'


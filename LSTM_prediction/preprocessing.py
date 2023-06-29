# Created by asorova

import yaml
import pandas as pd
import os
import warnings
import model_tuning
warnings.filterwarnings("ignore")


def get_config():
    with open("./../config.yaml", 'r') as stream:
        config = yaml.safe_load(stream)
    return config


def read_data():
    config = get_config()
    dir_to = config['directory_to']
    file_name_to = config['cleared_data_to']
    return pd.read_csv(os.path.join(dir_to, file_name_to), parse_dates=['Event Date'])


def select_column_for_prediction(cleared_data, prediction):
    if prediction == 'demand':
        return cleared_data[['Event Date', 'Sub-Category', 'Event', 'Region']].dropna(how='any')
    elif prediction == 'price':
        return cleared_data[['Event Date', 'Sub-Category', 'Event', 'Euro Price/Kg']].dropna(how='any')
    else:
        raise Exception("Wrong prediction type. Use prediction=demand or prediction=price")


def get_data_for_time_series_analysis(cleared_data, event_type='all', category='all', region='all', prediction='demand'):
    cleared_data = select_column_for_prediction(cleared_data, prediction)
    if event_type != 'all':
        cleared_data = cleared_data[cleared_data['Event'] == event_type]
    if category != 'all':
        cleared_data = cleared_data[cleared_data['Sub-Category'] == category]
    cleared_data = cleared_data.drop(columns=['Event', 'Sub-Category'])
    if prediction == 'demand':
        if region != 'all':
            cleared_data = cleared_data[cleared_data['Region'] == region]
        cleared_data = cleared_data.groupby('Event Date')['Region'].count()
        cleared_data = cleared_data.reset_index()
        cleared_data = cleared_data.rename(columns={'Region': 'Launches'})
    else:
        cleared_data = cleared_data.groupby(['Event Date']).mean()
        cleared_data = cleared_data.reset_index()
        cleared_data = cleared_data.rename(columns={'Euro Price/Kg': 'Prices'})
    return cleared_data[:-2], cleared_data['Event Date'][:-2]


def main():
    cleared_data = read_data()
    y, dates = get_data_for_time_series_analysis(cleared_data, 'New Product', 'Bread & Bread Products', 'West Europe', 'demand')
    # y, dates = get_data_for_time_series_analysis(cleared_data, prediction='price')
    model_tuning.predict(y, dates, look_back=10, epochs=80, prediction='demand', pred_num=6, retune=False)


if __name__ == "__main__":
    main()


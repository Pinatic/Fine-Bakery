# Created by asorova

import yaml
import pandas as pd
import os
import warnings
from LSTM_prediction import model_tuning

warnings.filterwarnings("ignore")


def get_config(config_file):
    with open(config_file, 'r') as stream:
        config = yaml.safe_load(stream)
    return config


def read_data(config):
    file_dir = config['directory_from']
    matching_data_file = config['data_matching_claim_file']
    return pd.read_csv(os.path.join(file_dir, matching_data_file), parse_dates=['Event Date'])


def get_data_for_time_series_analysis(cleared_data, event_type='all', category='all', region='all', prediction='demand'):
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


def do_analysis(config_file, prediction, region, pred_num, tune):
    config = get_config(config_file)
    cleared_data = read_data(config)

    file_dir = config['directory_from']
    predictions_file = config['predictions_table']
    predictions_plot = config['predictions_plot']
    save_predictions_to = os.path.join(file_dir, predictions_file)
    save_plot_to = os.path.join(file_dir, predictions_plot)

    y, dates = get_data_for_time_series_analysis(cleared_data, 'New Product', 'all', region, prediction)
    return model_tuning.predict(y, dates, save_predictions_to, save_plot_to, look_back=10, epochs=100, prediction=prediction, pred_num=pred_num, retune=tune)


# demand - for claims prediction, price - for price prediction
if __name__ == "__main__":
    do_analysis("./../config.yaml", 'demand', 'West Europe', 6, False)


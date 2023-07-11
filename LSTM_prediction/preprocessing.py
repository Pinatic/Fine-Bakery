"""In this module the data according to the prediction type - 'demand' or 'price' - is selected, LSTM model is tuned,
predictions are made and resulting plot and the table with future values are persisted on the local machine

By: Anna Sorova
"""

import yaml
import pandas as pd
import os
import warnings
from LSTM_prediction import model_tuning_and_predictions

warnings.filterwarnings("ignore")


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


def read_data(config):
    """
    Read dataframe

    Args:
        config (any): config object

    Returns:
        df (dataframe): returns dataframe corresponding to certain claim category
    """
    file_dir = config['directory_from']
    matching_data_file = config['data_matching_claim_file']
    return pd.read_csv(os.path.join(file_dir, matching_data_file), parse_dates=['Event Date'])


def get_data_for_time_series_analysis(cleared_data, event_type='all', category='all', region='all', prediction='demand'):
    """
    Select data corresponding to the input parameters

    Args:
        cleared_data (dataframe): original data corresponding to the certain claim category
        event_type(str): type of event happened to the product (for example, new launch or import)
        category(str): category of the product
        region(str): region of the product consumption (for example, East Europe)
        prediction(str): type of prediction - 'demand' for demand prediction, 'price' for price prediction

    Returns:
        x (list): x values for the trend prediction corresponding to the input parameters
        y (list): y value for the trend prediction (datestamps)
    """
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
    """
    Selects data corresponding to the input parameters, tunes the LSTM model, makes predictions, persists resulting plot
    and the table with future values on the local machine

    Args:
        config_file (str): path to the config file
        prediction(str): type of prediction - 'demand' for demand prediction, 'price' for price prediction
        region(str): region of the product consumption (for example, East Europe)
        pred_num(int): number of future values to predict
        tune(bool): indicates if the model should be automatically tuned

    Returns:
        fig (figure): returns matplotlib figure that can be shown on the screen
    """
    config = get_config(config_file)
    cleared_data = read_data(config)

    file_dir = config['directory_from']
    predictions_file = config['predictions_table']
    predictions_plot = config['predictions_plot']
    save_predictions_to = os.path.join(file_dir, predictions_file)
    save_plot_to = os.path.join(file_dir, predictions_plot)

    y, dates = get_data_for_time_series_analysis(cleared_data, 'New Product', 'all', region, prediction)
    return model_tuning.predict(y, dates, save_predictions_to, save_plot_to, look_back=10, epochs=100, prediction=prediction, pred_num=pred_num, retune=tune)


if __name__ == "__main__":
    do_analysis("./../config.yaml", 'demand', 'West Europe', 6, False)


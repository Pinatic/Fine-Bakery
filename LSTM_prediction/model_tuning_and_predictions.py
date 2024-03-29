"""In this module LSTM model is tuned, predictions are made and resulting plot and the table with future values are
persisted on the local machine

By: Anna Sorova
"""

import numpy as np
import matplotlib.pyplot as plt
from scikeras.wrappers import KerasRegressor
import tensorflow as tf
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from datetime import datetime
from dateutil.relativedelta import relativedelta
import os
import csv
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '5'
tf.random.set_seed(7)


def create_dataset(dataset, look_back=1):
    """
    For each data point starting with the N+1 datapoint this function returns the list of the N
    previous observations (where N = loop back) as the first output parameter and the current observation as the
    second output parameter.

    Args:
        dataset (sized): original data corresponding to the certain claim category
        look_back(int): number of past observations used as predictors

    Returns:
        x (list): list of lists of N previous observations
        y (list): current observations starting from N+1 datapoint
    """
    dataX, dataY = [], []
    for i in range(len(dataset)-look_back):
        a = dataset[i:(i+look_back), 0]
        dataX.append(a)
        dataY.append(dataset[i + look_back, 0])
    return np.array(dataX), np.array(dataY)


def get_dataset(dataset, prediction):
    """
    Get the values to be predicted according to the prediction type ('demand' for the demand prediction, 'price' for
    the price prediction)

    Args:
        dataset (sized): original data corresponding to the certain claim category
        prediction(str): type of prediction ('demand' or 'price')

    Returns:
        x (list): values to be predicted
    """
    if prediction == 'demand':
        return dataset['Launches']. values
    elif prediction == 'price':
        return dataset['Prices']. values
    else:
        raise Exception("Wrong prediction type. Use prediction=demand or prediction=price")


def create_model(look_back, neurons, recurrent_dropout):
    """
    Create a one-layered LSTM model considering input parameters

    Args:
        look_back (int): number of past observations to be used as predictors
        neurons(int): number of neurons to be used in the LSTM layer
        recurrent_dropout(int): recurrent dropout rate for the LSTM layer

    Returns:
        model (obj): ML model
    """
    model = Sequential()
    model.add(LSTM(neurons, input_shape=(1, look_back), recurrent_dropout=recurrent_dropout))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    return model


def predict(y, dates, save_predictions_to, save_plot_to, look_back=10, epochs=100, prediction='demand', pred_num=6, retune=False):
    """
    Creates the LSTM model, tunes it if needed, makes predictions and persists resulting plot and the table with
    future values on the local machine.

    Args:
        y(list): data to be predicted
        dates(list): list of corresponding timestamps
        save_predictions_to (str): path to the file where the table with the future predictions should be saved
        save_plot_to(str): path to the file where the plot with the future predictions should be saved
        look_back (int): number of past observations to be used as predictors
        epochs(int): number of epochs to use in the LSTM model
        prediction(str): type of prediction - 'demand' for demand prediction, 'price' for price prediction
        pred_num(int): number of future values to predict
        retune(bool): indicates if the model should be automatically tuned

    Returns:
        fig (figure): returns matplotlib figure that can be shown on the screen
    """
    if not retune:
        return train_and_predict(y, dates, save_predictions_to, save_plot_to, look_back=look_back, epochs=epochs, prediction=prediction, pred_num=pred_num)
    dataset = get_dataset(y, prediction).astype('float32')
    reshaped_dataset = dataset.reshape(-1, 1)
    scaler = MinMaxScaler(feature_range=(0, 1))
    dataset = scaler.fit_transform(reshaped_dataset)
    X_all, Y_all = create_dataset(dataset, look_back)
    X_all = np.reshape(X_all, (X_all.shape[0], 1, X_all.shape[1]))
    best_params = tune_model(X_all, Y_all, epochs)
    return train_and_predict(y, dates, save_predictions_to, save_plot_to, look_back=best_params['model__look_back'], epochs=epochs, prediction=prediction, pred_num=pred_num, neurons=best_params['model__neurons'], dropout=best_params['model__recurrent_dropout'])


def tune_model(X, y, epochs):
    """
    LSTM model is created and tuned using GridSearchCV

    Args:
        X (sized): normalized and preprocessed list of N previous observations where N is the number of past
    observations used as predictors
        y(sized): current observations starting from N+1 datapoint where N is the number of past
    observations used as predictors
        epochs(int): number of epochs to use in the LSTM model

    Returns:
        best_params_ (list): list of the best parameters for the model
    """
    model = KerasRegressor(model=create_model, epochs=epochs, batch_size=10, verbose=0)
    look_backs = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    neurons = [4, 5, 6, 7, 8]
    recurrent_dropout = [0.0, 0.1, 0.2, 0.3]
    param_grid = dict(model__look_back=look_backs, model__neurons=neurons, model__recurrent_dropout=recurrent_dropout)
    test_size = int(len(X) * 0.33)
    tscv = TimeSeriesSplit(n_splits=3, test_size=round(test_size))
    grid = GridSearchCV(estimator=model, param_grid=param_grid, n_jobs=-1, cv=tscv)
    grid_result = grid.fit(X, y)
    print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
    return grid_result.best_params_


def train_and_predict(dataset, dates, save_predictions_to, save_plot_to, look_back=10, epochs=100, prediction='demand', pred_num=6, neurons=4, dropout=0.0):
    """
    Creates the LSTM model with provided parameters, makes predictions and persists resulting plot and the table with
    future values on the local machine.

    Args:
        dataset(list): data to be predicted
        dates(list): list of corresponding timestamps
        save_predictions_to (str): path to the file where the table with the future predictions should be saved
        save_plot_to(str): path to the file where the plot with the future predictions should be saved
        look_back (int): number of past observations to be used as predictors
        epochs(int): number of epochs to use in the LSTM model
        prediction(str): type of prediction - 'demand' for demand prediction, 'price' for price prediction
        pred_num(int): number of future values to predict
        neurons(int): number of neurons to be used in the LSTM layer
        dropout(int): recurrent dropout rate for the LSTM layer

    Returns:
        fig (figure): returns matplotlib figure that can be shown on the screen
    """
    dataset = get_dataset(dataset, prediction)
    dataset = dataset.astype('float32')
    reshaped_dataset = dataset.reshape(-1, 1)
    scaler = MinMaxScaler(feature_range=(0, 1))
    dataset = scaler.fit_transform(reshaped_dataset)

    train_size = int(len(dataset) * 0.67)
    train, test = dataset[0:train_size,:], dataset[train_size-look_back:len(dataset), :]

    trainX, trainY = create_dataset(train, look_back)
    testX, testY = create_dataset(test, look_back)

    trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
    testX = np.reshape(testX, (testX.shape[0], 1, testX.shape[1]))

    model = Sequential()
    model.add(LSTM(neurons, input_shape=(1, look_back), recurrent_dropout=dropout))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(trainX, trainY, epochs=epochs, batch_size=1, verbose=2)

    trainPredict = model.predict(trainX)
    testPredict = model.predict(testX)

    trainPredict = scaler.inverse_transform(trainPredict)
    trainY = scaler.inverse_transform([trainY])
    testPredict = scaler.inverse_transform(testPredict)
    testY = scaler.inverse_transform([testY])

    trainScore = np.sqrt(mean_squared_error(trainY[0], trainPredict[:,0]))
    # print('Train Score: %.2f RMSE' % (trainScore))
    testScore = np.sqrt(mean_squared_error(testY[0], testPredict[:,0]))
    # print('Test Score: %.2f RMSE' % (testScore))

    predictions, datetimes = make_predictions(pred_num, look_back, dataset, dates, model, scaler)
    save_predictions_to_csv(predictions, datetimes, pred_num, save_predictions_to)
    return make_plot(dataset, datetimes, save_plot_to, trainPredict, testPredict, trainScore, testScore, predictions, scaler, look_back, prediction)


def make_plot(dataset, datetimes, save_plot_to, trainPredict, testPredict, trainScore, testScore, predictions, scaler, look_back, prediction):
    """
    Creates plot of the actual data, predicted value for the both training and testing datasets and the predicted
    future values. Persists plot on the local machine.

    Args:
        dataset(list): data to be predicted
        datetimes(list): list of corresponding timestamps
        save_plot_to(str): path to the file where the plot with the future predictions should be saved
        trainPredict(list): predicted training dataset
        testPredict(list): predicted testing dataset
        trainScore(int): mean_squared_error of the predicted training dataset
        testScore(int): mean_squared_error of the predicted testing dataset
        predictions(list): list of the predicted future values
        scaler(obj): scaler used for scaling dataset before training the model.
        look_back (int): number of past observations to be used as predictors
        prediction(str): type of prediction - 'demand' for demand prediction, 'price' for price prediction

    Returns:
        fig (figure): returns matplotlib figure that can be shown on the screen
    """
    predictoinsPlot = np.empty_like(dataset[:-1])
    predictoinsPlot[:, :] = np.nan
    first_val = scaler.inverse_transform(dataset[-1].reshape(-1, 1))
    predictoinsPlot = np.append(predictoinsPlot, np.append(first_val, predictions))

    trainPredictPlot = np.empty_like(dataset)
    trainPredictPlot[:, :] = np.nan
    trainPredictPlot[look_back:len(trainPredict) + look_back, :] = trainPredict

    testPredictPlot = np.empty_like(dataset)
    testPredictPlot[:, :] = np.nan
    testPredictPlot[len(trainPredict) + look_back:len(dataset), :] = testPredict

    inbetween = np.empty_like(dataset)
    inbetween[:, :] = np.nan
    inbetween[len(trainPredict) + look_back - 1:len(trainPredict) + look_back + 1, :] = [trainPredict[-1],
                                                                                             testPredict[0]]
    fig = plt.figure(figsize=(20, 8))
    ax = fig.add_subplot(1, 1, 1)

    actuals = np.append(scaler.inverse_transform(dataset),
                        np.zeros(len(datetimes) - len(scaler.inverse_transform(dataset))) * np.nan)
    ax.plot(datetimes, actuals, label='Actual')

    trains = np.append(trainPredictPlot, np.zeros(len(datetimes) - len(trainPredictPlot)) * np.nan)
    ax.plot(datetimes, trains, label='Train set: RMSE = ' + str(round(trainScore, 2)))

    tests = np.append(testPredictPlot, np.zeros(len(datetimes) - len(testPredictPlot)) * np.nan)
    ax.plot(datetimes, tests, label='Test set: RMSE = ' + str(round(testScore, 2)))

    inbetweens = np.append(inbetween, np.zeros(len(datetimes) - len(inbetween)) * np.nan)
    ax.plot(datetimes, inbetweens, linestyle='dashed', color='blue', alpha=0.5)

    ax.plot(datetimes, predictoinsPlot, color='blue', linewidth=3, label='Predictions')

    ax.axvline(x=datetimes[len(dataset) - 1], color='r', linestyle='dotted', label='current state')

    ax.legend(loc='lower right')
    if prediction == 'demand':
        ylabel = 'Launches'
        title = 'LSTM user demand prediction'
    else:
        title = 'LSTM product price prediction'
        ylabel = 'Prices'
    ax.set_title(title)
    ax.set_xlabel('Months')
    ax.set_ylabel(ylabel)
    fig.savefig(save_plot_to, dpi=1200)
    return fig


def save_predictions_to_csv(predictions, dates, pred_num, file_to_save):
    """
    Saves predicted future values table to the file on the local machine

    Args:
        predictions(list): list of the predicted future values
        dates(list): list of corresponding timestamps
        pred_num(int): number of future values to predict
        file_to_save(str): path to the file where the table with the future predictions should be saved
    """
    table = {}
    for count, date in enumerate(dates[-pred_num:]):
        table[date] = str(predictions[count])
    with open(file_to_save, 'w', encoding='UTF8') as f:
        w = csv.writer(f)
        w.writerows(map(lambda x: [x[0], x[1]], table.items()))


def get_data_times(number, dates):
    """
    Gets the list of the timestamps for the actual values and the future values

    Args:
        number(int): number of future values to predict
        dates(list): list of corresponding timestamps
    Returns:
        l (list): list of timestamps for the actual values and the future values
    """
    d = dates[len(dates)-1]
    list_dates = [d + relativedelta(months=+month_num) for month_num in range(1, number+1)]
    return np.append([date for date in dates], list_dates)


def make_predictions(number, look_back, dataset, dates, model, scaler):
    """
    Makes predictions using trained model

    Args:
        number(int): number of future values to predict
        look_back (int): number of past observations to be used as predictors
        dataset(list): actual data used for model training and testing
        dates(list): list of actual timestamps
        model(obj): trained LSTM model
        scaler(obj): scaler used for scaling dataset before training the model.

    Returns:
        actuals (list): list of the actual values and the future values
        dates(list): list of timestamps for the actual values and the future values
    """
    actuals = []
    last_observations = dataset[-look_back:]
    last_observations = last_observations.reshape(1, -1)
    last_observations = np.reshape(last_observations, (last_observations.shape[0], 1, last_observations.shape[1]))
    for i in range(number):
        new_predict = model.predict(last_observations)
        new_actual = scaler.inverse_transform(new_predict)
        actuals.append(new_actual.ravel()[0])
        last_observations = np.append(last_observations[:,:,1:], new_predict)
        last_observations = last_observations.reshape(1, -1)
        last_observations = np.reshape(last_observations, (last_observations.shape[0], 1, last_observations.shape[1]))
    dates = get_data_times(number, dates)
    return actuals, dates

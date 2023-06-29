# Created by asorova

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
    dataX, dataY = [], []
    for i in range(len(dataset)-look_back):
        a = dataset[i:(i+look_back), 0]
        dataX.append(a)
        dataY.append(dataset[i + look_back, 0])
    return np.array(dataX), np.array(dataY)


def get_dataset(dataset, prediction):
    if prediction == 'demand':
        return dataset['Launches']. values
    elif prediction == 'price':
        return dataset['Prices']. values
    else:
        raise Exception("Wrong prediction type. Use prediction=demand or prediction=price")


def create_model(look_back, neurons, recurrent_dropout):
    model = Sequential()
    model.add(LSTM(neurons, input_shape=(1, look_back), recurrent_dropout=recurrent_dropout))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    return model


def predict(y, dates, save_predictions_to, look_back=10, epochs=100, prediction='demand', pred_num=6, retune=False):
    if not retune:
        return train_and_predict(y, dates, save_predictions_to, look_back=look_back, epochs=epochs, prediction=prediction, pred_num=pred_num)
    dataset = get_dataset(y, prediction).astype('float32')
    reshaped_dataset = dataset.reshape(-1, 1)
    scaler = MinMaxScaler(feature_range=(0, 1))
    dataset = scaler.fit_transform(reshaped_dataset)
    X_all, Y_all = create_dataset(dataset, look_back)
    X_all = np.reshape(X_all, (X_all.shape[0], 1, X_all.shape[1]))
    best_params = tune_model(X_all, Y_all, epochs)
    train_and_predict(y, dates, save_predictions_to, look_back=best_params['model__look_back'], epochs=epochs, prediction=prediction, pred_num=pred_num, neurons=best_params['model__neurons'], dropout=best_params['model__recurrent_dropout'])


def tune_model(X, y, epochs):
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


def train_and_predict(dataset, dates, save_predictions_to, look_back=10, epochs=100, prediction='demand', pred_num=6, neurons=4, dropout=0.0):
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
    make_plot(dataset, datetimes, trainPredict, testPredict, trainScore, testScore, predictions, scaler, look_back, prediction)


def make_plot(dataset, datetimes, trainPredict, testPredict, trainScore, testScore, predictions, scaler, look_back, prediction):
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
    plt.figure(figsize=(20, 8))

    actuals = np.append(scaler.inverse_transform(dataset),
                        np.zeros(len(datetimes) - len(scaler.inverse_transform(dataset))) * np.nan)
    plt.plot(datetimes, actuals, label='Actual')

    trains = np.append(trainPredictPlot, np.zeros(len(datetimes) - len(trainPredictPlot)) * np.nan)
    plt.plot(datetimes, trains, label='Train set: RMSE = ' + str(round(trainScore, 2)))

    tests = np.append(testPredictPlot, np.zeros(len(datetimes) - len(testPredictPlot)) * np.nan)
    plt.plot(datetimes, tests, label='Test set: RMSE = ' + str(round(testScore, 2)))

    inbetweens = np.append(inbetween, np.zeros(len(datetimes) - len(inbetween)) * np.nan)
    plt.plot(datetimes, inbetweens, linestyle='dashed', color='blue', alpha=0.5)

    plt.plot(datetimes, predictoinsPlot, color='blue', linewidth=3, label='Predictions')

    plt.axvline(x=datetimes[len(dataset) - 1], color='r', linestyle='dotted', label='current state')

    plt.legend(loc='lower right')
    if prediction == 'demand':
        title = 'LSTM user demand prediction'
    else:
        title = 'LSTM product price prediction'
    plt.gca().set(title=title, xlabel='Months', ylabel='Launches')
    plt.show()


def save_predictions_to_csv(predictions, dates, pred_num, file_to_save):
    table = {}
    for count, date in enumerate(dates[-pred_num:]):
        table[date] = str(predictions[count])
    with open(file_to_save, 'w', encoding='UTF8') as f:
        w = csv.writer(f)
        w.writerows(map(lambda x: [x[0], x[1]], table.items()))


def get_data_times(number, dates):
    d = dates[len(dates)-1]
    list_dates = [d + relativedelta(months=+month_num) for month_num in range(1, number+1)]
    return np.append([date for date in dates], list_dates)


def make_predictions(number, look_back, dataset, dates, model, scaler):
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

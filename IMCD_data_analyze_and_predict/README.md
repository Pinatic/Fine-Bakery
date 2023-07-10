Code in this directory was created for testing purposes. 

The `IMCD_data_preprocessing.ipynb` file is responsible for data parsing, cleaning, plotting and analyzing. 
The parser clears out all the non-ASCII symbols and some punctuation marks from string data types, gets the numbers according to certain regular expressions out of the columns that are expected to be float or integer, and converts the columns to their predefined data types, which are specified in the metadata. The metadata represents a field in a configuration file structured as a list of pairs where the first value is a column name and the second one is a data type that the column should be converted to. 
It collects the statistics about the separate files and the final cleaned file such as the number of columns, rows, unique and missing values in each column.
The word cloud using the most popular words from the 'Product name' column is created. There was an attempt to clean the recipies column for future use.

The `ARIMA_regression_analysis.ipynb` file is responsible for analyzing and preprocessing the data for the ARIMA model. The relation between the event date and the pricing, and between the event date and the product categories in different regions is studied. Missing values are checked and processed.
Since data represents a monthly time series the plots were created to see if data follows a certain repetitive pattern every year.
The stationarity of data was established. AutoCorrelation Function plot was created to check the correlation between the past and current observations. Granger causality test was conducted to see if one time series will be useful to forecast another. The ARIMA model
was manually and automatically tuned. Future values were predicted and two validation techniques were used - walk forward validation and out-of-time cross validation.


The `LSTM_forecast.ipynb` file is responsible for building the LSTM model, tuning it and making predictions. The dataset is split into the training and testing sets, which constitutes 67% and 33% of the data, respectively. The model seeks to minimize the mean squared error (MSE) and employs an Adam optimization algorithm. After the model is trained on the training dataset, it predicts the values of the testing datasets for model validation purposes and a defined number of future points. To assess the accuracy of predictions for both training and testing datasets, the root mean square error (RMSE) is used. 


Files in this directory are not called from the main script.

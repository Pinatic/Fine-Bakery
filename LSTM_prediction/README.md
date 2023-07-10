Code in this directory is called from the main script and is a part of the trend prediction pipeline.

The `preprocessing.py` file is responsible for selecting the data according to the prediction type - 'demand' or 'price'. If flag "-t", "--type" is set to 'demand', the number of new launches per month is calculated and saved for the future trend analysis. Therefore, the number of new launches (user demand) for the selected claim per month will be predicted. 
If the flag "-t" is set to 'price', the average monthly price of products belonging to the selected claim is calculated and is used for the future analysis. Thus, the average monthly price of the products will be predicted. 

The `model_tuning_and_predictions.py` file is responsible for the automatic one-layered LSTM model tuning if the -tu (--tune) command line parameter is set to True. 
If it is set to False, the model is trained with the default values: look_back (number of past observations used as predictors) = 10, epochs = 100, recurrent_dropout = 0.0, neurons in a layer = 4. After defining model hyperparameters, it is trained.
The dataset is split into the training and testing sets, which constitutes 67% and 33% of the data, respectively. The model seeks to minimize the mean squared error (MSE) and employs an Adam optimization algorithm. After the model is trained on the training dataset, it predicts the values of the testing datasets for model validation purposes and a defined number of future points. To assess the accuracy of predictions for both training and testing datasets, the root-mean-square error (RMSE) is used.
The predictions are plotted alongside the actual values and saved on a local machine. Predicted values are saved in a table and persisted as well for future use.


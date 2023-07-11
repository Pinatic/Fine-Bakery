# Fine-Bakery

Alternatives to animal-based products are getting more popular, and the supply chain is weakening. This leads to a higher demand for food producers to offer alternative ingredients in recipes while retaining the product's qualities. Meeting the evolving demands of customers has become an increasingly intricate task since the process of finding suitable substitutes requires a deep understanding of the chemical and sensory properties of the ingredient and any potential substitutes. This project was created to help with this task.

Firstly, we propose and evaluate a method for predicting suitable replacement ingredients using a network created with NetworkX and embedded using node2vec based on Euclidean distance. Secondly, we aim to create and evaluate a robust predictive model for trend predictions using a Long Short-Term Memory (LSTM) neural network. 

## Set up virtual environment

To run the script in this directory you have to use certain Python modules. Please create your own virtual environment with the modules listed in requirements.txt to execute the applications.

After you have created your environment and activated it, please install the requirements in this environment with the command:

    pip install -r requirements.txt

## Trend prediction

The proprietary data received from IMCD contains information about the products released by the company and their characteristics, such as the product category, country of the end customer, product price, and the date of a new product’s launch. To predict user demand patterns, time series data of newly launched products was used. An average monthly price of the products within one claim category was used for the product affordability prediction.

To run trend prediction pipeline you should run the main.py script in the root directory. It performs several steps in a strict order.

### Trend prediction pipeline:

1) Parsing and cleaning raw data. Code responsible for this functionality can be found in the `parser/XML_parser.py` and `parser/merge_and_inspect.py`files.
2) Claim categorization. Corresponding code can be found in the `parser/categorizer.py` file.
3) Selecting data matching the claim category. Code responsible for this functionality can be found in the `parser/data_selector.py`.
4) ML model tuning and making predictions with persisting the results (trend plot and table with predicted values) on the local machine. Corresponding code can be found in the `LSTM_prediction/preprocessing.py` and `LSTM_prediction/model_tuning.py` files.

To run the script, the configuration file should be correctly set up.

Please set the values of `"directory_from"`, `"popular_claims_file"`, `"predictions_table"`, `"predictions_plot"`, `"file_paths"`, `"delete_columns"`, `"directory_to"`, `"cleared_data_to"`, `"metadata"`, `"popular_claims_num"` fields in configuration file. Configuration file is called `./config.yaml` in the root directory.

### Explanation of the configuration parameters:
 
`"directory_from"` is the directory with the IMCD data containing the products information.

`"file_paths"` is a list of the file names in the `"directory_from"` directory to the IMCD data files.

`"delete_columns"` is a list of columns that do not carry any useful information for the data analysis. 

`"directory_to"` is a directory where the data statistics is gathered. This statistics is saved for every provided IMCD file after cleaning and parsing step. Also, the statistics of the final cleaned file is saved after all the IMCD data files were cleaned and merged into one file. In case it is impossible to merge the IMCD data into one file, the errors encountered by merging these files will be stored in this directory as well.

`"cleared_data_to"` is a file name of the final cleaned file - the result of merging all the cleaned IMCD data files into one file.

`"metadata"` is a list of rules to parse the IMCD data files. It defines the data types of certain columns. In the parsing step columns from this list are converted into the defined data types.

`"popular_claims_num"` is the number of the top most popular claims found in the data.

Claims categories are saved in the `"directory_from"/"popular_claims_file"` file.

Data matching certain claim is saved in `"directory_from"/"data_matching_claim_file"` file.

Predictions table is saved in `"directory_from"/"predictions_table"` file.

Predictions plot is saved in `"directory_from"/"predictions_plot"` file.

To run the script you should provide the command line flags to the script. 

### Command line flags:

"-p", "--parse" (default=False) - Whether to clean, parse and write all the data sources into one file used for the analysis. It is recommended to use if the original data was enriched with more data.

"-c", "--categorize" (default=False) - Whether to regenerate the list of most popular claims. It is recommended to be True if the '--parse' flag is set to True. If '--parse' flag is set to False, '--categorize' flag may be set to True in case the desirable number of the most popular claims was changed in the config file.

"-t", "--type" (default='demand') - Two possible values: ['demand', 'price']. The type of predictions to make. If set to 'demand', the number of new launches (user demand) for the selected claim per month will be predicted. If set to 'price', the average price of products belonging to the selected claim per month will be predicted. 

"-cl", "--claim" (default=None, required=True) - Products containing this claim in their list of claims will be used for analysis. This claim should be one of the most popular claims.

"-r", "--region" (default='all') - Three possible values: ['West Europe', 'East Europe', 'all']. Products in selected region will be used for analysis. If set to 'all', prediction is made for categories in both East and West regions.

"-tu", "--tune" (default=False) - Whether to tune the model with different parameters to get the most reliable predictions. Takes more time as compared to training the model with predefined parameters. It is recommended to be True if the original data was enriched with more data and either of flags '--categorize' or '--parse' is set to True.

"-n", "--numPred" (default=6) - The number of data points to be predicted in the future.

### Commands to start an application

To start an application for the first time, use the command:

    python3 main.py -p -c -t='demand' -cl='recyclable packaging' -r='West Europe' -tu -n=6

Next time if the data was not enriched and config file was not changed, parameters -p and -c can be omitted to boost the performance of the application. Parameter -tu is recommended to be always set. Corresponding command:

    python3 main.py -t='demand' -cl='recyclable packaging' -r='West Europe' -tu -n=6

## Ingredient replacement

To get the suitable replacement for the certain ingredient, run the `nested_functionality.py` script in the Back_end directory. Before running the script, provide the config.json file in the Back_end directory with the access key to ChatGPT API and the path to the file containing the functionalities list of replacement candidates for a given ingredient. Run the script with the comand:

    python3 nested_functionality.py -i='Egg'

where the flag -i (--ingredient) represents the ingredient to be replaced.
    
    

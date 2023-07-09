# Fine-Bakery

Please set the values of `"directory_from"`, `"popular_claims_file"`, `"predictions_table"`, `"predictions_plot"`, `"file_paths"`, `"delete_columns"`, `"directory_to"`, `"cleared_data_to"`, `"metadata"`, `"popular_claims_num"` fields in config file. Config file is called `./config.yaml`.
 
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

"-p", "--parse" (default=False) - Whether to clean, parse and write all the data sources into one file used for the analysis. It is recommended to use if the original data was enriched with more data.

"-c", "--categorize" (default=False) - Whether to regenerate the list of most popular claims. It is recommended to be True if the '--parse' flag is set to True. If '--parse' flag is set to False, '--categorize' flag may be set to True in case the desirable number of the most popular claims was changed in the config file.

"-t", "--type" (default='demand') - Two possible values: ['demand', 'price']. The type of predictions to make. If set to 'demand', the number of new launches (user demand) for the selected claim per month will be predicted. If set to 'price', the average price of products belonging to the selected claim per month will be predicted. 

"-cl", "--claim" (default=None, required=True) - Products containing this claim in their list of claims will be used for analysis. This claim should be one of the most popular claims.

"-r", "--region" (default='all') - Three possible values: ['West Europe', 'East Europe', 'all']. Products in selected region will be used for analysis. If set to 'all', prediction is made for categories in both East and West regions.

"-tu", "--tune" (default=False) - Whether to tune the model with different parameters to get the most reliable predictions. Takes more time as compared to training the model with predefined parameters. It is recommended to be True if the original data was enriched with more data and either of flags '--categorize' or '--parse' is set to True.

"-n", "--numPred" (default=6) - The number of data points to be predicted in the future.


Command to start an application for the first time:

    python3 main.py -p -c -t='demand' -cl='recyclable packaging' -r='West Europe' -tu -n=6

Next time if the data was not enriched and config file was not changed, parameters -p and -c can be omitted to boost the performance of the application. Parameter -tu is recommended to be always set.

    python3 main.py -t='demand' -cl='recyclable packaging' -r='West Europe' -tu -n=6

In the case of ingredient replacement download Back_end ,Download precomputed file ing_replace_result4 and config  from DSLS ,run nested_functionality.py
    
    

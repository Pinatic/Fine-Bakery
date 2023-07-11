# Ingredient Functionality Analysis

This script allows you to retrieve the functionality of replacement candidates for a given ingredient using the OpenAI Chat API. It provides a way to analyze ingredient replacements based on their functionality in a specific context.

## Setup

1. Install the required packages:

   
   pip install requests tabulate


2. Obtain an API key from OpenAI. Follow the OpenAI documentation to create an account and generate an API key.

3. Place the script in the same directory as the `config.json` file, which contains the necessary configuration.

## Functionality

The script provides the following functionality:

### 1. Retrieve Ingredient Functionality

The `get_ingredient_functionality` function retrieves the functionality of replacement candidates for a given ingredient. It uses the OpenAI Chat API to generate responses based on user queries about the functionality of ingredient replacements.

To use this function, specify the ingredient for which you want to find replacement candidates. The function retrieves the replacement candidates from a JSON file (`ing_replace_result4.json`) and sends queries to the Chat API to get the functionality information.

The resulting functionality information, along with the candidate name and distance, is displayed in a tabular format.

## Usage

To use the script, follow these steps:

1. Ensure that the `config.json` file is properly configured with the necessary API key and other settings.

2. Run the script:

   
  functionality_tableshow.py
   

3. The script will retrieve the functionality of replacement candidates for the specified ingredient and display the results in a tabular format.

   Example usage:

   
   get_ingredient_functionality("Milk")
   

   This will retrieve the functionality information for replacement candidates of "Milk" as specified in the `ing_replace_result4.json` file.

## Notes

- The script uses the OpenAI Chat API, so make sure you have a valid API key and the necessary permissions to access the API.
- The `ing_replace_result4.json` file should contain the replacement candidates for each ingredient. Adjust the file path as needed.
- The script includes a delay of 30 seconds between API requests to comply with OpenAI's rate limits. You can adjust this delay if needed.
- The resulting functionality information is displayed in a tabular format using the `tabulate` library.


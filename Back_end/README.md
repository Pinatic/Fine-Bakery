# Ingredient Functionality Analyzer

The Ingredient Functionality Analyzer is a tool that helps identify the functionality of replacement candidates for a given ingredient in bakery products. It utilizes the OpenAI GPT-3.5-turbo language model to generate responses based on user queries.
## Requirements
Ensure you have the following dependencies installed:

- Python 3.x
- aiohttp
- tabulate
- nest_asyncio
- internet connection to communicate with the OpenAI API and retrieve functionality information.
- API key
## Setup

1. Install the required dependencies by running `pip install -r requirements.txt`.
2. Obtain an API key from OpenAI. Make sure to have it available for authentication.

## Configuration

Update the `config.json` file with your OpenAI API key and other relevant information:

json
{
    "API_KEY": "YOUR_API_KEY",
    "functionalities_file_path": "path/to/functionalities.json"
}


- `API_KEY`: Your OpenAI API key.
- `functionalities_file_path`: The file path to the JSON file containing replacement candidates and their functionalities.

## Usage

Run the analyzer with the following command:

python main.py -i <ingredient>


Replace `<ingredient>` with the ingredient you want to analyze. The analyzer will retrieve the replacement candidates for the specified ingredient from the `functionalities.json` file and analyze their functionality using the OpenAI GPT-3.5-turbo model.

The analyzer will display a table showing the top five replacement candidates along with their distances and functionalities.

## Customization

- `functionalities.json`: Update this file with your own replacement candidates and their corresponding functionalities. The file should follow the structure:

json
{
    "ingredient1": [
        {
            "candidate": "replacement1",
            "distance": 0.5
        },
        {
            "candidate": "replacement2",
            "distance": 0.7
        },
        ...
    ],
    "ingredient2": [
        {
            "candidate": "replacement3",
            "distance": 0.2
        },
        ...
    ],
    ...
}


- Adjust the `temperature` value in the `get_functionality` method (inside `FlavorDataScraper` class) to modify the response randomness. Higher values (e.g., 0.7) result in more random responses, while lower values (e.g., 0.2) make the responses more focused and deterministic.




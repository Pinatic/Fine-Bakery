import asyncio
import nest_asyncio
import json
from tabulate import tabulate
import aiohttp
import argparse
import sys

nest_asyncio.apply()
import json

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

API_KEY = config.get('API_KEY')
functionalities_file_path = config.get('functionalities_file_path')
url = 'https://api.openai.com/v1/chat/completions'
header = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {API_KEY}'
}


async def get_functionality(session, ingredient, replacement):
    """
    Retrieves the functionality of a replacement candidate for a given ingredient.
    
    Args:
        session (aiohttp.ClientSession): The HTTP client session.
        ingredient (str): The ingredient to replace.
        replacement (dict): The replacement candidate.
    
    Returns:
        dict: A dictionary containing the candidate, distance, and functionality.
            If the functionality cannot be determined, None is returned.
    """
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "user",
             "content": f"functionality of {replacement['candidate']} as an {ingredient} replacement in bakery!"}
        ],
        "temperature": 0.7
    }

    async with session.post(url, headers=header, data=json.dumps(data)) as response:
        response_json = await response.json()
        try:
            answer = response_json['choices'][0]['message']['content']
            tokens = answer.split()
            functionality_keywords = []
            for i in range(len(tokens) - 1):
                if tokens[i].istitle() and tokens[i + 1].lower() in ["agent:", "retention:", "texture:"]:
                    functionality_keywords.append(tokens[i])
            return {
                'candidate': replacement['candidate'],
                'distance': replacement.get('distance', 'N/A'),
                'functionality': ', '.join(
                    functionality_keywords) if functionality_keywords else 'No specific functionality'
            }
        except KeyError:
            return None


async def get_ingredient_functionality(ingredient):
    """
    Retrieves the functionality of replacement candidates for a given ingredient.
    
    Args:
        ingredient (str): The ingredient to replace.
    """
    with open(functionalities_file_path, 'r') as file:
        ingredient_dict = json.load(file)

    replacements = ingredient_dict.get(ingredient, [])
    if not replacements:
        print(f"No replacement candidates found for {ingredient}.")
        return

    print(f"{ingredient}:")

    async with aiohttp.ClientSession() as session:
        tasks = []

        for replacement in replacements:
            tasks.append(get_functionality(session, ingredient, replacement))

        results = await asyncio.gather(*tasks)
        results = [result for result in results if result is not None]

        sorted_results = sorted(results, key=lambda x: x['distance'])

        table_headers = ['Candidate', 'Distance', 'Functionality']
        table_data = [[result['candidate'], result['distance'], result['functionality']] for result in sorted_results]

        print(tabulate(table_data[:5], headers=table_headers, tablefmt='grid'))


def run_ingredient_functionality(ingredient):
    """
    Runs the functionality analysis for a given ingredient.
    
    Args:
        ingredient (str): The ingredient to analyze.
    """
    asyncio.run(get_ingredient_functionality(ingredient))


def parse_args(args):
    """
        Parses the command line arguments

        Args:
            args (list): Command line parameters
        """
    parser = argparse.ArgumentParser(
        description="Set an ingredient"
    )
    parser.add_argument(
        "-i",
        "--ingredient",
        type=str,
        required=True,
        help="The ingredient for which the suitable replacements should be found"
    )
    return parser.parse_args(args)


def main(args=None):
    args = parse_args(args)
    run_ingredient_functionality(args.ingredient)


if __name__ == "__main__":
    sys.exit(main())

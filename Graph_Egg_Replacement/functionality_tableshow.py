import requests
import time
import json
from tabulate import tabulate
import json

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

API_KEY = config.get('API_KEY')
url = 'https://api.openai.com/v1/chat/completions'
header = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {API_KEY}'
}

def get_ingredient_functionality(ingredient):
    """
    Retrieves the functionality of replacement candidates for a given ingredient.
    
    Args:
        ingredient (str): The ingredient to replace.
    """
    with open('ing_replace_result4.json', 'r') as file:
        ingredient_dict = json.load(file)

    result = []  # List to store the results

    replacements = ingredient_dict.get(ingredient, [])
    if not replacements:
        print(f"No replacement candidates found for {ingredient}.")
        return

    print(f"{ingredient}:")
    
    # Counter for the number of candidates processed
    candidate_count = 0
    
    table_headers = ['Candidate', 'Distance', 'Functionality']
    table_data = []
    
    for replacement in replacements:
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "user", "content": f"functionality of {replacement['candidate']} as an {ingredient} replacement in bakery!"}
            ],
            "temperature": 0.7
        }

        response = requests.post(url, headers=header, data=json.dumps(data))
        response_json = response.json()

        try:
            # Extract the generated answer from the API response
            answer = response_json['choices'][0]['message']['content']

            # Tokenize the answer
            tokens = answer.split()

            # Extract functionality keywords
            functionality_keywords = []
            for i in range(len(tokens) - 1):
                if tokens[i].istitle() and tokens[i + 1].lower() in ["agent:", "retention:", "texture:"]:
                    functionality_keywords.append(tokens[i])

            # Add the data to the table
            table_data.append([
                replacement['candidate'],
                replacement.get('distance', 'N/A'),
                ', '.join(functionality_keywords) if functionality_keywords else 'No specific functionality'
            ])
            
            # Increment the candidate count
            candidate_count += 1
            
            # Break the loop if the desired number of candidates has been reached (5 in this case)
            if candidate_count == 5:
                break

        except KeyError:
            pass

        # Wait for 30 seconds before making another API request
        time.sleep(30)

    # Print the table
    print(tabulate(table_data, headers=table_headers, tablefmt='grid'))


# Example usage
get_ingredient_functionality("Milk")

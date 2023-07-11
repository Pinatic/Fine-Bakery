# IngredientReplacer

The `IngredientReplacer` is a Python class that allows you to find ingredient replacements based on ingredient distances and category data. It provides a flexible and customizable solution for ingredient substitution in recipes or other culinary applications. This README file will guide you through the setup and usage of the `IngredientReplacer` class.

## Prerequisites

Before using the `IngredientReplacer` class, ensure that you have the following:

- Python 3.x installed on your system.

## Requirements

The `IngredientReplacer` class has the following dependencies:

- Python 3.x
- json

 install the required dependencies 

## Setup

To set up and use the `IngredientReplacer` class, follow these steps:

1. Clone or download the repository to your local machine.

2. Prepare the configuration file and data files:

   - Create a configuration file (`config.json`) with the following structure:

    json
     {
       "ingredients_category": "ingredient_category_data.json",
       "distance_files": [
         ["distance_file1.txt", "distance_file2.txt"],
         
         ...
       ]
     }
     

     - `"ingredients_category"`: The path to the ingredient category data file (in JSON format).
     - `"distance_files"`: A list of pairs of distance files (in text format) used for ingredient replacements.

   - The `ingredient_category_data.json`  contains ingredient category data. Each entry should have the following format:

     json
     [
       {
         "name": "Ingredient 1",
         "category": ["Category A", "Category B", ...]
       },
       {
         "name": "Ingredient 2",
         "category": ["Category C", "Category D", ...]
       },
       ...
     ]
     


   - Prepare the distance files (text format) that contain ingredient distances. Each line should have the following format:

 

3. Import the `IngredientReplacer` class in your Python script or interactive Python environment:

   python
   from ingredient_replacer import IngredientReplacer
   

## Usage

The `IngredientReplacer` class provides the following methods for finding ingredient replacements:

- `load_config(config_file)`: Loads the configuration from a JSON file.
- `load_ingredient_category_data(file_path)`: Loads the ingredient category data from a JSON file.
- `filter_ingredients(ingredient_category_data)`: Filters ingredients based on excluded categories.
- `load_distance_file(distance_file)`: Loads ingredient distances from a text file.
- `find_replacements(ingredient, ingredient_distances)`: Finds replacements for a given ingredient.
- `rank_candidates(unique_candidates)`: Ranks the unique candidates based on their frequency and distance.
- `calculate_frequency(candidates, ingredient)`: Calculates the frequency of candidates for a given ingredient.
- `save_results(filename, unique_candidates, ingredient)`: Saves the results to a file.
- `process_ingredients()`: Processes the list of ingredients and finds replacements.
- `run()`: Executes the ingredient replacement process.

To use the `IngredientReplacer` class, create an instance of it by passing the path to the configuration file as a parameter:

python
replacer = IngredientReplacer("config.json")


You can then run the ingredient replacement process by calling the `run()` method:


replacer.run()


The results will be saved in a file named `ing_replace_result.json`.

## Customization

You can customize the behavior of the `IngredientReplacer` class by modifying the configuration file (`config.json`) and adjusting the code in the class methods. For example, you can modify the excluded categories list or adjust the number of replacements to be found.

Feel free to explore and modify the code according to your specific requirements.

## Conclusion

The `IngredientReplacer` class provides a powerful and flexible solution for finding ingredient replacements. By following the setup instructions and utilizing the provided methods, you can easily integrate the ingredient replacement functionality into your own Python projects and applications.
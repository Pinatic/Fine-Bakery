# Scoring the graph embedings

Scoring the graph embedings  is a set of scripts that allow you to find ingredient replacements based on ingredient distances and category data. This README file provides instructions on how to use the scripts.

## Prerequisites

Before running the scripts, make sure you have the following:

- Python 3.x installed on your system.
- Required dependencies: `numpy`, `scikit-learn`, and `pickle`.

You can install the dependencies by running the following command:


pip install numpy scikit-learn


## Usage

### Step 1: Extract Ingredient Names and Categories

The first script (`extract_ingredients`) extracts ingredient names and categories from a JSON file. Follow these steps:

1. Update the path to your input JSON file (`integrated_data.json`) in the script.
2. Specify the desired output file path in the `output_file` variable.
3. Run the script:

   python extract_ingredients.py


4. The script will extract the ingredient names and categories and save them to the specified output file (`ingredients.json`).

### Step 2: Calculate Euclidean Distances

The second script (`calculate_and_save_euclidean_distance`) calculates the Euclidean distances between ingredient embeddings and saves the results to a file. Follow these steps:

1. Place your ingredient embedding file (in pickle format, `*.pkl`) in the specified location.
2. Update the path to your ingredient embedding file in the script.
3. Specify the desired output file path in the `output_file` variable.
4. Run the script:


   python calculate_and_save_euclidean_distances
 

5. The script will calculate the Euclidean distances between ingredient embeddings and save them to the specified output file (`distance_table.txt`).

### Step 3: Find Ingredient Replacements

The third script (`find_replacements`) finds ingredient replacements based on the calculated distances and category data. Follow these steps:

1. Update the input variables in the script:
   - `ingredient`: The ingredient for which you want to find replacements.
   - `ingredient_distances_file`: The path to the file containing ingredient distances.
   - `ingredient_category_file`: The path to the file containing ingredient category data (`ingredients.json`).
2. Run the script:

   python find_replacements.py


3. The script will print the replacements for the specified ingredient, excluding the input ingredient and any replacements with a distance of 0.0.
All code in this and subfolders is written by Lillie sadat hosseini japalagh If there are any questions you can contact me at g.s.hosseini.japalagh@st.hanze.nl

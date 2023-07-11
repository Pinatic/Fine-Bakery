# Ingredient Analysis and Replacement

This script provides functionalities for analyzing ingredients, extracting data, and finding ingredient replacements based on distances and categories. It utilizes JSON files, network graphs, embeddings, and distance calculations.

## Setup

1. Install the required packages:

  
   pip install networkx matplotlib requests colorama tabulate node2vec
   

2. Place the script in the same directory as the `config.json` file, which contains the necessary configuration.

## Functionality

### 1. Integrate JSON Data

The `integrate_json_data` function integrates multiple JSON files into a single JSON file, combining ingredient data from different sources.

### 2. Extract Ingredient Names

The `extract_ingredient_names` function extracts ingredient names from the integrated JSON file and saves them to a separate file.

### 3. Extract Ingredients and Categories

The `extract_ingredients_category` function extracts ingredient names and categories from the integrated JSON file and saves them to a separate file.

### 4. Draw Graph from Pickle

The `draw_graph_from_pickle` function loads a graph from a pickle file and visualizes it using NetworkX and Matplotlib.

### 5. Generate Node Embeddings

The `generate_node_embeddings` function generates node embeddings using Node2Vec and saves them to a file.

### 6. Calculate and Save Euclidean Distances

The `calculate_and_save_euclidean_distances` function calculates Euclidean distances between ingredient embeddings and saves them to a file.

### 7. Load Distance File

The `load_distance_file` function loads ingredient distances from a file and returns them as a dictionary.

### 8. Find Ingredient Replacements

The `find_ingredient_replacements` function finds ingredient replacements based on distances, ingredient categories, and a target ingredient.

## Usage

To use the script, follow these steps:

1. Ensure that the `config.json` file is properly configured with the necessary paths and settings.

2. Choose the desired functionality by uncommenting the corresponding function call in the `main` function.

3. Run the script:

   Replacement_Ingredient.py
  

## Example

Here's an example usage scenario:

1. Run the `integrate_json_data` function to integrate multiple JSON files into a single JSON file.

2. Run the `extract_ingredient_names` function to extract ingredient names from the integrated JSON file.

3. Run the `extract_ingredients_category` function to extract ingredient names and categories from the integrated JSON file.

4. Run the `draw_graph_from_pickle` function to load a graph from a pickle file and visualize it.

5. Run the `generate_node_embeddings` function to generate node embeddings using Node2Vec.

6. Run the `calculate_and_save_euclidean_distances` function to calculate Euclidean distances between ingredient embeddings and save them to a file.

7. Run the `find_ingredient_replacements` function to find ingredient replacements based on distances and categories for a target ingredient.

Please note that some functions may require specific files or configurations to be present. Ensure that the necessary files and configurations are available before running the corresponding functions.

All code in this and subfolders is written by Lillie sadat hosseini japalagh If there are any questions you can contact me at g.s.hosseini.japalagh@st.hanze.nl

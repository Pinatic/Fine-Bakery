import json
import networkx as nx
import matplotlib.pyplot as plt
import os
import sys
import pickle
from node2vec import Node2Vec
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances
import requests
import time
from colorama import Fore, Style

def integrate_json_data():
    """
    Integrate multiple JSON files into a single JSON file.
    """
    # Load configuration from a config file
    with open("config.json", "r") as config_file:
        config = json.load(config_file)

    # Specify the folder path containing the JSON files
    folder_path = config.get("ingredients", "")

    # Check if the output file already exists
    data = config.get("data", "")
    if os.path.exists(data):
        os.remove(data)

    # Create a dictionary to store the integrated data
    integrated_data = []

    # Iterate over each file in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)

            # Read the JSON file
            with open(file_path, "r") as file:
                file_data = json.load(file)
                ingredient = file_data.get("entity_alias_readable", "")
                molecules = file_data.get("molecules", [])
                category = file_data.get("category_readable", "")

                # Iterate over molecules and extract relevant data
                for molecule in molecules:
                    molecule_info = {
                        "flavor": molecule.get("flavor_profile", ""),
                        "molecule": molecule.get("common_name", ""),
                        "fooddb_flavor_profile": molecule.get("fooddb_flavor_profile", ""),
                        "taste": molecule.get("taste", "")
                    }
                    ingredient_data = {
                        "ingredients": ingredient,
                        "category": [category],
                        "molecules": [molecule_info]
                    }

                    # Check if ingredient already exists in integrated_data
                    existing_ingredient = next((item for item in integrated_data if item["ingredients"] == ingredient), None)

                    # If ingredient already exists, append molecule to existing ingredient
                    if existing_ingredient:
                        existing_ingredient["molecules"].append(molecule_info)
                    else:
                        integrated_data.append(ingredient_data)

    # Write the integrated data into the output file
    with open(data, "w") as my_file:
        json.dump(integrated_data, my_file, indent=4)

    print("Integrated JSON file created successfully.")

def extract_ingredient_names():
    """
    Extract ingredient names from the integrated JSON file and save them to a separate file.
    """
    # Load configuration from the config file
    with open("config.json", "r") as config_file:
        config = json.load(config_file)

    # Get the file path from the config
    file_path = config.get("data", "")

    # Read the file
    with open(file_path) as file:
        data = json.load(file)

    # Extract the ingredient names
    ingredient_names = [item['ingredients'] for item in data]

    # Check if the output file already exists
    output_file = config.get("ingredient_list", "")
    if os.path.exists(output_file):
        os.remove(output_file)

    # Write the ingredient names into the output file
    with open(output_file, "w") as output:
        json.dump(ingredient_names, output, indent=4)

def extract_ingredients_category():
    """
    Extract ingredient names and categories from the integrated JSON file and save them to a separate file.
    """
    # Load configuration from the config file
    with open("config.json", "r") as config_file:
        config = json.load(config_file)

    # Get the file path from the config
    file_path = config.get("data", "")

    # Read the file
    with open(file_path) as file:
        data = json.load(file)

    # Extract ingredient names and categories
    ingredients_category = []
    for ingredient in data:
        ingredient_name = ingredient['ingredients']
        ingredient_category = ingredient['category']
        ingredients_category.append({'name': ingredient_name, 'category': ingredient_category})

    # Check if the output file already exists
    output_file = config.get("ingredients_category", "")
    if os.path.exists(output_file):
        os.remove(output_file)

    # Write the data into the output file
    with open(output_file, "w") as output:
        json.dump(ingredients_category, output, indent=4)

def draw_graph_from_pickle(config_path, pickle_file_key):
    """
    Load a graph from a pickle file and draw it using NetworkX and Matplotlib.
    """
    # Load configuration from the config file
    with open(config_path, "r") as config_file:
        config = json.load(config_file)

    # Get the pickle file path from the config
    pickle_file_path = config.get(pickle_file_key, "")

    # Load the graph from the pickle file
    with open(pickle_file_path, "rb") as pickle_file:
        graph = pickle.load(pickle_file)

    # Draw the graph
    plt.figure(figsize=(100, 80))
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_size=500, edge_color='gray')
    labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)

    # Display the graph
    plt.show()

def generate_node_embeddings(config_path, graph_key):
    """
    Generate node embeddings using Node2Vec and save them to a file.
    """
    # Load configuration from the config file
    with open(config_path, "r") as config_file:
        config = json.load(config_file)

    # Get the folder path from the config
    data = config.get("data", "")

    # Get the ingredients file path from the folder path
    ingredients_file_path = os.path.join(data)
    with open(ingredients_file_path, "r") as file:
        data = json.load(file)

    ingredients = []

    for ingredient in data:
        ingredient_dict = {
            'name': ingredient['ingredients'],
            'molecules': [],
            'category': ingredient['category'],
        }

        for molecule in ingredient['molecules']:
            ingredient_dict['molecules'].append(molecule['molecule'])
        ingredients.append(ingredient_dict)

    print(ingredients)

    # Get the graph file path from the config
    graph_file_path = config.get(graph_key, "")

    # Load the graph from the pickle file
    with open(graph_file_path, "rb") as pickle_file:
        graph = pickle.load(pickle_file)

    # Generate random walks using Node2Vec with tuned parameters
    node2vec = Node2Vec(graph, dimensions=128, walk_length=80, num_walks=300)
    model = node2vec.fit(window=10, min_count=1)

    # Retrieve node embeddings for available ingredients
    ingredient_embeddings = {}
    for ingredient_dict in ingredients:
        ingredient_name = ingredient_dict['name']
        if ingredient_name in model.wv:
            embedding = model.wv[ingredient_name]
            ingredient_embeddings[ingredient_name] = embedding
        else:
            continue

    return ingredient_embeddings

def calculate_and_save_euclidean_distances(config_path, embedding_file, output_file):
    """
    Calculate Euclidean distances between ingredient embeddings and save them to a file.
    """
    with open(config_path, "r") as config_file:
        config = json.load(config_file)

    # Get the embedding file path from the config
    embedding_file_path = config.get(embedding_file, "")

    # Load the embeddings from the pickle file
    with open(embedding_file_path, "rb") as embedding_file:
        embedding = pickle.load(embedding_file)

    # Calculate Euclidean distance matrix
    ingredient_embeddings_list = list(embedding.values())
    euclidean_distance_matrix = euclidean_distances(ingredient_embeddings_list)

    # Get the list of ingredient names
    ingredient_names = list(embedding.keys())

    # Save the Euclidean distance matrix to a file
    with open(output_file, "w", encoding="utf-8") as file:
        for i, ingredient1 in enumerate(ingredient_names):
            for j, ingredient2 in enumerate(ingredient_names):
                distance = euclidean_distance_matrix[i, j]
                line = f"{ingredient1}, {ingredient2}: {distance}\n"
                file.write(line)


def load_distance_file(distance_file):
    """
    Load ingredient distances from a file and return them as a dictionary.
    """
    ingredient_distances = {}
    with open(distance_file, "r", encoding="utf-8") as file:
        for line in file:
            ingredients, distance = line.strip().split(":")
            ingredient1, ingredient2 = ingredients.split(",")
            distance = float(distance)

            if ingredient1 not in ingredient_distances:
                ingredient_distances[ingredient1] = {}
            if ingredient2 not in ingredient_distances:
                ingredient_distances[ingredient2] = {}

            ingredient_distances[ingredient1][ingredient2] = distance
            ingredient_distances[ingredient2][ingredient1] = distance

    return ingredient_distances

def find_replacements(ingredient, ingredient_distances, ingredient_category_data):
    """
    Find ingredient replacements based on distances, ingredient categories, and a target ingredient.
    """
    # Load ingredient categories from JSON data
    ingredient_categories = {}
    for ingredient_data in ingredient_category_data:
        ingredient_name = ingredient_data['name']
        categories = ingredient_data['category']
        ingredient_categories[ingredient_name] = categories

    # Get the distances for the input ingredient
    distances = ingredient_distances.get(ingredient, {})

    # Sort the distances in ascending order
    sorted_distances = sorted(distances.items(), key=lambda x: x[1])

    # Find the best 20 ingredient replacements with distances
    replacements = []
    for ingredient, distance in sorted_distances:
        ingredient_categories_list = ingredient_categories.get(ingredient.strip(), [])

        if ingredient_categories_list and all(category not in ingredient_categories_list for category in ['Meat', 'Seafood', 'Fish', 'Fungus', 'Dish', 'Additive']):
            replacements.append((ingredient, distance))

        # Break the loop when we have found 20 replacements
        if len(replacements) == 20:
            break

    return replacements


def find_ingredient_replacements(config_path, target_ingredient):
    # Load configuration from the config file
    with open(config_path, "r") as config_file:
        config = json.load(config_file)

    # Load the ingredient category data
    ingredient_category_data = config.get("ingredients_category", "")
    with open(ingredient_category_data, "r") as category_data:
        category_data = json.load(category_data)

    # Load the ingredient distances
    ingredient_distances = config.get("distance1", "")
    ingredient_distances = load_distance_file(ingredient_distances)

    # Find replacements for the target ingredient
    replacements = find_replacements(target_ingredient, ingredient_distances, category_data)

    # Prepare the result
    result = []
    for replacement, distance in replacements:
        if replacement != target_ingredient and distance != 0.0:
            result.append((replacement, distance))

    return result



def main():

    config_path = "config.json"  # Replace with your actual config file path
    graph_key = "pickle_file1"  # Replace with the key in the config file that contains the graph file path
    embedding_key ="embedding_graph1"
    target_ingredient ="Egg"
    draw_graph_from_pickle(config_path, graph_key)
    ingredient_embeddings = generate_node_embeddings(config_path, graph_key)
    calculate_and_save_euclidean_distances(config_path,embedding_key, ingredient_embeddings)
    find_ingredient_replacements(config_path,target_ingredient)



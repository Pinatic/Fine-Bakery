# Graph Constructor

Ingredient Graph Analysis

## Description

This project analyzes ingredient data to create a graph based on shared flavors, visualize the graph, and save/load the graph using Pickle. It aims to explore relationships between ingredients and understand their flavor similarities.

## Prerequisites

- Python 3.x
- Required packages: json, networkx, matplotlib, pickle

## Getting Started

1. Clone the repository:

   git clone https://github.com/your-username/your-repository.git


2. Install the required packages
   
   pip install json networkx matplotlib pickle
   

3. Prepare the JSON data:

   - Place the `integrated_data.json` file in the main directory of the Graph_FlavorDB.ipynb

4. Run the code:

   
   python code_file.py
   

## Code Explanation

### Part 1: Reading JSON Data and Creating Graph

This section of the code reads ingredient data from a JSON file and creates a graph based on shared flavors between ingredients.

- The code reads the ingredient data from the JSON file.
- It extracts the ingredient names, flavors, and categories from the data.
- An empty graph is created using the NetworkX library.
- Iterating over the ingredients, the code calculates the shared flavor counts with other ingredients.
- The top 10 ingredients with the most shared flavors are connected to each ingredient in the graph.

### Part 2: Drawing the Graph

This section of the code visualizes the created graph using matplotlib.

- The code uses matplotlib to draw the graph created in the previous section.
- It sets the figure size according to the desired dimensions.
- The spring layout algorithm is applied to the graph with a fixed seed for consistent layout generation.
- Nodes are drawn with colors based on their categories.
- Edges are drawn to connect the ingredients with shared flavors.
- Labels are added to the nodes to display the ingredient names.
- Additional category nodes are included to provide a legend for category colors.

### Part 3: Saving and Loading the Graph

This section of the code demonstrates how to save and load the created graph using the Pickle module.

- The code uses the Pickle module to save and load the created graph.
- After the graph is created in the previous sections, it is saved as a Pickle file (`graph_most_shared_flavors.pkl`).
- The Pickle file can be loaded and used later for further analysis or visualization.

## File Descriptions

- `code_file.py`: The Python script containing the code for reading JSON data, creating the graph, drawing the graph, and saving/loading the graph.
- `integrated_data.json`: The JSON file containing ingredient data, including names, flavors, and categories.
- `graph_most_shared_flavors.pkl`: Pickle file containing the created graph with shared flavor connections.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- The code in this project is inspired by various concepts and techniques in the fields of data analysis, graph theory, and network analysis.
- We acknowledge the authors and contributors of the libraries and packages used in this project for their valuable work.
All code in this and subfolders is written by Lillie sadat hosseini japalagh If there are any questions you can contact me at g.s.hosseini.japalagh@st.hanze.nl

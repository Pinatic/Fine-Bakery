import json


class IngredientReplacer:
    def __init__(self, config_file):
        """
        Initialize the IngredientReplacer.

        Args:
            config_file (str): The path to the configuration file.
        """
        self.config = self.load_config(config_file)
        self.ingredient_category_data = self.load_ingredient_category_data(self.config["ingredients_category"])
        self.ingredients_list = self.filter_ingredients(self.ingredient_category_data)
        self.distance_files = self.config["distance_files"]

    @staticmethod
    def load_config(config_file):
        """
        Load the configuration from a JSON file.

        Args:
            config_file (str): The path to the configuration file.

        Returns:
            dict: The configuration data.
        """
        with open(config_file, "r") as file:
            return json.load(file)

    @staticmethod
    def load_ingredient_category_data(file_path):
        """
        Load the ingredient category data from a JSON file.

        Args:
            file_path (str): The path to the ingredient category data file.

        Returns:
            dict: The ingredient category data.
        """
        with open(file_path, "r") as file:
            return json.load(file)

    @staticmethod
    def filter_ingredients(ingredient_category_data):
        """
        Filter the ingredients based on the excluded categories.

        Args:
            ingredient_category_data (list): The list of ingredient category data.

        Returns:
            list: The filtered list of ingredient names.
        """
        exclude_categories = ['Meat', 'Seafood', 'Fish', 'Fungus', 'Dish']

        filtered_ingredients = [
            item['name'] for item in ingredient_category_data if not any(category in item['category'] for category in
                                                                         exclude_categories)
        ]

        return filtered_ingredients

    @staticmethod
    def load_distance_file(distance_file):
        """
        Load the ingredient distances from a text file.

        Args:
            distance_file (str): The path to the distance file.

        Returns:
            dict: The ingredient distances.
        """
        ingredient_distances = {}
        with open(distance_file, "r", encoding="ISO-8859-1") as file:
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

    def find_replacements(self, ingredient, ingredient_distances):
        """
        Find replacements for a given ingredient based on ingredient distances and category data.

        Args:
            ingredient (str): The ingredient to find replacements for.
            ingredient_distances (dict): The ingredient distances.

        Returns:
            list: The list of replacements and their distances.
        """
        distances = ingredient_distances.get(ingredient, {})
        sorted_distances = sorted(distances.items(), key=lambda x: x[1])
        exclude_categories = ['Meat', 'Seafood', 'Fish', 'Fungus', 'Dish']
        replacements = []
        for ingredient, distance in sorted_distances:
            for ingredient_data in self.ingredient_category_data:
                ingredient_name = ingredient_data['name']
                ingredient_categories_list = ingredient_data['category']

                if (
                    ingredient.strip() == ingredient_name.strip()
                    and all(category not in ingredient_categories_list for category in exclude_categories)
                ):
                    replacements.append((ingredient, distance))
                    break

            if len(replacements) == 13:
                break

        return replacements

    @staticmethod
    def rank_candidates(unique_candidates):
        """
        Rank the unique candidates based on their frequency and distance.

        Args:
            unique_candidates (list): The list of unique candidates.

        Returns:
            list: The ranked list of candidates.
        """
        frequency_groups = {}
        for c in unique_candidates:
            freq = c['freq']
            if freq in frequency_groups:
                frequency_groups[freq].append(c)
            else:
                frequency_groups[freq] = [c]

        ranked_candidates = []
        sorted_groups = sorted(
            frequency_groups.values(), key=lambda x: x[0]['freq'], reverse=True
        )
        for group in sorted_groups:
            group.sort(key=lambda x: x['distance'])
            ranked_candidates.extend(group)

        return ranked_candidates

    @staticmethod
    def calculate_frequency(candidates, ingredient):
        """
        Calculate the frequency of candidates for a given ingredient.

        Args:
            candidates (list): The list of candidates and their distances.
            ingredient (str): The ingredient for which to calculate the frequency.

        Returns:
            list: The list of unique candidates with their frequency.
        """
        unique_candidates = []
        ingredient_frequencies = {}

        for replacement, distance in candidates:
            if replacement != ingredient and distance != 0.0:
                if replacement in ingredient_frequencies:
                    ingredient_frequencies[replacement] += 1
                else:
                    ingredient_frequencies[replacement] = 1

                unique_candidates.append(
                    {
                        'ingredient': replacement,
                        'distance': distance,
                        'freq': ingredient_frequencies[replacement],
                    }
                )

        return unique_candidates

    @staticmethod
    def save_results(filename, unique_candidates, ingredient):
        """
        Save the results to a file.

        Args:
            filename (str): The name of the output file.
            unique_candidates (list): The list of unique candidates.
            ingredient (str): The ingredient for which the replacements were found.
        """
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(f"Replacements for {ingredient}:\n")
            file.write("Top 10 replacements and their Scores:\n")
            for candidate in unique_candidates[:10]:
                line = "- {} (Distance: {}) - Frequency: {} - Score: {}\n".format(
                    candidate['ingredient'],
                    candidate['distance'],
                    candidate['freq'],
                    candidate['score']
                )
                file.write(line)

    def process_ingredients(self):
        """
        Process the list of ingredients and find replacements.

        Returns:
            dict: A dictionary containing the replacements for each ingredient.
        """
        results_dict = {}
        total_ingredients = len(self.ingredients_list)

        for index, ingredient in enumerate(self.ingredients_list, 1):
            try:
                print(f"Processing ingredient {index}/{total_ingredients}: {ingredient}")

                for distance_file1, distance_file2 in self.distance_files:
                    ingredient_distances1 = self.load_distance_file(distance_file1)
                    ingredient_distances2 = self.load_distance_file(distance_file2)
                    replacements1 = self.find_replacements(ingredient, ingredient_distances1)
                    replacements2 = self.find_replacements(ingredient, ingredient_distances2)
                    candidates = replacements1 + replacements2
                    unique_candidates = self.calculate_frequency(candidates, ingredient)

                    ranked_candidates = self.rank_candidates(unique_candidates)
                    out_list = [
                        {
                            'candidate': candidate['ingredient'],
                            'distance': candidate['distance'],
                        }
                        for candidate in ranked_candidates[:10]
                    ]
                    results_dict[ingredient] = out_list
            except Exception as e:
                print(f"An error occurred for ingredient '{ingredient}': {e}")
                continue

        return results_dict

    def run(self):
        """
        Run the ingredient replacement process.
        """
        results_dict = self.process_ingredients()
        with open("ing_replace_result4.json", "w") as file:
            json.dump(results_dict, file, indent=4)


if __name__ == "__main__":
    replacer = IngredientReplacer("config.json")
    replacer.run()

import urllib.request
import json


class FlavorDataScraper:
    """
    A class to scrape flavor data from FlavorDB and store it in a JSON file.
    """

    def __init__(self):
        self.flavors_data = {}
        self.missing_JSON_files = []

    def flavordb_entity_url(self, entity_id):
        """
        Returns the URL for a specific JSON file based on the entity ID.

        Args:
            entity_id (int): The ID of the entity.

        Returns:
            str: The URL of the JSON file.
        """
        return f"https://cosylab.iiitd.edu.in/flavordb/entities_json?id={entity_id}"

    def get_flavordb_entity(self, entity_id):
        """
        Retrieves and parses a JSON file from the specified URL and returns it as a dictionary.

        Args:
            entity_id (int): The ID of the entity.

        Returns:
            dict or None: The parsed JSON data as a dictionary or None if the URL does not exist.
        """
        try:
            with urllib.request.urlopen(self.flavordb_entity_url(entity_id)) as url:
                return json.loads(url.read().decode())
        except urllib.error.HTTPError:
            print("URL does not exist, skipping...")
            return None

    def filter_molecules_entity(self, molecule):
        """
        Filters and selects specific columns from the molecule dictionary.

        Args:
            molecule (dict): The molecule data.

        Returns:
            dict: The filtered molecule data.
        """
        filtered_molecule = {
            'Functional Groups': molecule.get('functional_groups'),
            'FoodDB ID': molecule.get('fooddb_id'),
            'Common Name': molecule.get('common_name'),
            'PubChem ID': molecule.get('pubchem_id'),
            'Flavor Profile': molecule.get('flavor_profile')
        }
        return filtered_molecule

    def filter_flavordb_entity(self, entity):
        """
        Filters and selects specific columns from the entity dictionary.

        Args:
            entity (dict): The entity data.

        Returns:
            dict: The filtered entity data.
        """
        filtered_flavour = {
            'Name': entity.get('natural_source_name'),
            'Category': entity.get('category'),
            'Entity ID': entity.get('entity_id'),
            'Alias': entity.get('entity_alias_readable'),
            'Molecules': {}
        }
        for molecule in entity.get('molecules', []):
            molecule_name = molecule.get('common_name')
            filtered_flavour['Molecules'][molecule_name] = self.filter_molecules_entity(molecule)
        return filtered_flavour

    def scrape_flavor_data(self, num_entities=1001):
        """
        Scrapes flavor data from FlavorDB, filters it, and stores it in a JSON file.

        Args:
            num_entities (int): The number of entities to scrape. Defaults to 1001.
        """
        for entity_id in range(num_entities):
            try:
                entity = self.get_flavordb_entity(entity_id)
                if entity:
                    filtered_flavour = self.filter_flavordb_entity(entity)
                    flavor_name = filtered_flavour['Name']
                    self.flavors_data[flavor_name] = filtered_flavour
                else:
                    self.missing_JSON_files.append(entity_id)
            except Exception:
                self.missing_JSON_files.append(entity_id)
                continue

            # Show progress
            progress = (entity_id + 1) / num_entities * 100
            print(f"Scraping entity {entity_id}/{num_entities-1} [{progress:.2f}%]")

        with open("scrapped_ingredients.json", 'w') as json_file:
            json.dump(self.flavors_data, json_file, indent=4)

        print(f"Missing JSON files: {self.missing_JSON_files}")


def main():
    """
    The main function that runs the flavor data scraping.
    """
    scraper = FlavorDataScraper()
    scraper.scrape_flavor_data()


if __name__ == "__main__":
    main()

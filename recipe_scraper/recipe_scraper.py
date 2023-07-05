"""
In this module the RecipeScraper class is defined. 
This class is used to scrape recipes from a website. It uses a list of recipe
identiefiers to scrape the recipes. This list can be created using the classes
inside the 'recipe_identifier_fetchers.py' module.

By: Jacob Menzinga
Date: 05-07-2023
Version: 2.0
"""
import json
import os
from recipe_scrapers import scrape_me


class RecipeScraper:
    """
    Scrapes recipes from a website.
    """

    def __init__(self, folder, base_url, recipe_identifier_txt) -> None:
        """
        Args:
            folder (str): location where the recipes will be stored
            base_url (str): base recipe url of the website you want to scrape
            recipe_identifier_txt (str): location of the txt file
                                         containing the recipe identifiers
        """
        self.folder = folder
        self.base_url = base_url
        self.recipe_identifier_txt = recipe_identifier_txt

    def create_list(self):
        """
        Creates a list of recipe identifiers from a txt file.

        Returns:
            recipe_list (list): a list of unique recipe identifiers
        """
        with open(self.recipe_identifier_txt, 'r') as recep_file:
            recipe_list = recep_file.readline()
            recipe_list = recipe_list.replace("''", "', '")
            recipe_list = recipe_list.replace("'", "").split(', ')
            recipe_list = list(set(recipe_list))
            return recipe_list

    def scrape_recipe(self, recep):
        """
        gets a recipe based on the base_url and the recipe identifier

        Args:
            recep (str): the unique identifier of a recipe
        """
        filename = '_'.join(recep.lower().split())+'.json'
        print(filename)

        if os.path.isfile(self.folder+filename) is False:
            # print(f'{base_url}{recep}')
            try:
                scraper = scrape_me(self.base_url+recep)
                #  print(base_url+recep)

                if not os.path.exists(self.folder):
                    os.makedirs(self.folder)

                with open(self.folder+filename, 'w') as output:
                    js = scraper.to_json()
                    json.dump(js, output, indent=4)

            except Exception:
                # if something goes wrong, just skip the recipe
                pass

        else:
            print('Recipe already scraped.')

import json
import os
import pandas as pd
import numpy as np
from recipe_scrapers import scrape_me
import time


folder = '/commons/dsls/fine_bakery/scraped_recipes/smul/smul_receps/'
base_url = 'https://www.smulweb.nl/recepten/'
recipe_num_txt = '/commons/dsls/fine_bakery/scraped_recipes/smul/smulweb_recep_nrs.txt'


def create_list():
    with open(recipe_num_txt, 'r') as recep_file:
        recipe_list = recep_file.readline()
        recipe_list = recipe_list.replace("''", "', '")
        recipe_list = recipe_list.replace("'", "").split(', ')
        recipe_list = list(set(recipe_list))

        return recipe_list


def fetch_receps(recep):
    "gets the receps in a recep list"
    filename = '_'.join(recep.lower().split())+'.json'
    print(filename)

    if os.path.isfile(folder+filename) is False:
        # print(f'{base_url}{recep}')
        try:
            scraper = scrape_me(base_url+recep)
            #  print(base_url+recep)

            if not os.path.exists(folder):
                os.makedirs(folder)

            with open(folder+filename, 'w') as output:
                js = scraper.to_json()
                json.dump(js, output, indent=4)

        except Exception:
            pass

    else:
        print('Recipe already scraped.')
        pass


class scrape_recipes_mp:
    """
    Scrapes all the recipes found in a list of recipe urls and stores them in
    seperate json files using the recipe name in the supplied list as name

    attributes:
    folder (str): The location where the recipes should be stored
    base_url (str): The base url that refers to the website you want to scrape
    recipe_num_txt (csv file): A csv file containing the page,list of recipes of a
    scraped site
    """

    def __init__(self, folder, base_url, recipe_num_txt) -> None:
        folder = folder
        base_url = base_url
        recipe_num_txt = recipe_num_txt
        recipe_list = None

    def create_list(self):
        with open(recipe_num_txt, 'r') as recep_file:
            recipe_list = recep_file.readline()
            recipe_list = recipe_list.replace("''", "', '")
            recipe_list = recipe_list.replace("'", "").split(', ')
            recipe_list = list(set(recipe_list))

    def fetch_receps(recipe_list):
        n = 0
        "gets the receps in a recep list"
        for recep in recipe_list:
            filename = '_'.join(recep.lower().split())+'.json'

            if os.path.isfile(folder+"/"+filename) is False:
                # print(f'{base_url}{recep}')
                try:
                    scraper = scrape_me(base_url+recep)
                    print(base_url+recep)

                    if not os.path.exists(folder):
                        os.makedirs(folder)

                    with open(folder+"/"+filename, 'w') as output:
                        js = scraper.to_json()
                        json.dump(js, output, indent=4)

                        # A counter to keep track of the nr of recipes scraped
                        n += 1
                        print(f'{n} recipes scraped')

                        # time.sleep(2)  # To not overask the servers

                except Exception:
                    # Trying it again after a minute might solve some problems.
                    # It didn't. How i fix?
                    time.sleep(60)
                    continue

            else:
                print('Recipe already scraped.')
                continue

        print('Done')

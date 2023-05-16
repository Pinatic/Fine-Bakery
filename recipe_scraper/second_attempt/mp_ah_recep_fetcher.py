import json
import os
import pandas as pd
import numpy as np
from recipe_scrapers import scrape_me
import time


folder = '/commons/dsls/fine_bakery/scraped_recipes/ah/ah_receps/'
base_url = 'https://www.ah.nl/allerhande/recept/R-R'
recipe_num_txt = '/commons/dsls/fine_bakery/scraped_recipes/ah/ah_recep_nrs.txt'


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

import time
import json
import os
from recipe_scrapers import scrape_me


def scrape_recipes(folder, base_url, recipe_list):
    """
    Scrapes all the recipes found in a list of recipe urls and stores them in
    seperate json files using the recipe title as filepath and..........
    """
    n = 0

    for recep in recipe_list:
        filename = '_'.join(recep.lower().split())+'.json'

        if os.path.isfile(folder+"/"+filename) is False:
            scraper = scrape_me(f'{base_url}{recep}')

            if not os.path.exists(folder):
                os.makedirs(folder)

            with open(folder+"/"+filename, 'w') as output:
                js = scraper.to_json()
                json.dump(js, output, indent=4)

                n += 1
                print(f'{n} recipes scraped')

                time.sleep(2) # To not overask the servers

        else:
            print('Recipe already scraped.')
            continue
        
# Extend this to include a csv writer i think.
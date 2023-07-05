import json
import os
from recipe_scrapers import scrape_me


class RecipeScraper:

    def __init__(self, folder, base_url, recipe_identifier_txt) -> None:
        self.folder = folder
        self.base_url = base_url
        self.recipe_identifier_txt = recipe_identifier_txt
        self.recipe_identiefs = None

    def create_list(self):
        with open(self.recipe_identifier_txt, 'r') as recep_file:
            recipe_list = recep_file.readline()
            recipe_list = recipe_list.replace("''", "', '")
            recipe_list = recipe_list.replace("'", "").split(', ')
            recipe_list = list(set(recipe_list))
            self.recipe_identiefs = recipe_list

    def scrape_recipes(self, recep):
        "gets the receps in a recep list"
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
                pass

        else:
            print('Recipe already scraped.')
            pass

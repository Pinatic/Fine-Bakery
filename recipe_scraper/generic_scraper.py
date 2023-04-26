from recipe_scrapers import scrape_me
import json


def scrape_recipes(folder, base_url, recipe_list):
    """
    Scrapes all the recipes found in a list of recipe urls and stores them in
    seperate json files using the recipe title as filepath and..........
    """
    n = 0

    for recp_num in recipe_list[:2]:
        scraper = scrape_me(f'{base_url}{recp_num}')
        filename = '_'.join(scraper.title().lower().split())+'.json'

        with open(folder+"/"+filename, 'w') as output:
            js = scraper.to_json()
            json.dump(js, output, indent=4)

            n += 1
            print(f'{n} recipes scraped')

# Extend this to include a csv writer i think.
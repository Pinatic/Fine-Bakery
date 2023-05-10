from scrapers import *

folder = 'recipe_scraper/second_attempt/test/'

# Get recipe nr's from smulweb

smul = SmulwebScraper()
smul.get_numbers(destination=folder, start_at=1)

folder = 'recipe_scraper/second_attempt/test/'
recipe_csv = folder+'smulweb_recep_nrs.csv'

scraper = scrape_recipes(folder+'receps/', smul.base_recipe_url, recipe_csv)
scraper.create_list()
scraper.fetch_receps()

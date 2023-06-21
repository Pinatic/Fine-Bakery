from scraper_module import *

folder = 'recipe_scraper/second_attempt/test/ls/'

# Get recipe nr's from website
ls_receps = LekkerEnSimpelScraper()
ls_receps.get_recipes(destination=folder, start_at=1)

# Setting recep store location
ls_recipe_file = folder+'ls_recep_nrs.txt'

# Scraping the recipes
ls_scraper = scrape_recipes(folder+'ls_receps/', ls_receps.base_recipe_url,
                            ls_recipe_file)
ls_scraper.create_list()
ls_scraper.fetch_receps()

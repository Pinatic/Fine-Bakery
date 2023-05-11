from scrapers import *

folder = 'recipe_scraper/second_attempt/test/'

# Get recipe nr's from websites

smul_receps = SmulwebScraper()
smul_receps.get_numbers(destination=folder, start_at=1)

ls_receps = LekkerEnSimpelScraper()
ls_receps.get_numbers(destination=folder, start_at=1)

ah_receps = AlbertScraper()
ah_receps.get_numbers(destination=folder, start_at=0)

# Setting recep store location
smul_recipe_file = folder+'smulweb_recep_nrs.txt'
ls_recipe_file = folder+'ls_recep_nrs.txt'
ah_recipe_file = folder+'ah_recep_nrs.txt'

# Scraping the recipes
smul_scraper = scrape_recipes(folder+'receps/', smul_receps.base_recipe_url, 
                              smul_recipe_file)
smul_scraper.create_list()
smul_scraper.fetch_receps()

ls_scraper = scrape_recipes(folder+'receps/', ls_receps.base_recipe_url, 
                            ls_recipe_file)
ls_scraper.create_list()
ls_scraper.fetch_receps()

ah_scraper = scrape_recipes(folder+'receps/', ah_receps.base_recipe_url,
                            ls_recipe_file)
ah_scraper.create_list()
ah_scraper.fetch_receps()
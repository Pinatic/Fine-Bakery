from lekker_simpel_scraperV2 import LekkerSimpelScraper
from generic_recep_scraper import scrape_recipes
import time

def main():
    print('Scraping Lekker Simpel')
    l_s_scraper = LekkerSimpelScraper()
    l_s_scraper.get_recipes()
    scrape_recipes('recipe_scraper/ls_receps',
                   l_s_scraper.base_recep_url,
                   l_s_scraper.recipes)

if __name__ == '__main__':
    start = time.time()
    main()
    print(f'runtime: {time.time() - start}s')

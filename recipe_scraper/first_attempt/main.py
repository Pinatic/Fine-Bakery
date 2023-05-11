from albert_scraperV3 import AlbertScraper
from lekker_simpel_scraper import LekkerSimpelScraper
from recipe_scraper.smulweb_scraper import SmulwebScraper
from generic_recep_scraper import scrape_recipes
import time

def main():
    print('Scraping Albert Hein')
    ah_scraper = AlbertScraper()
    ah_scraper.get_numbers()
    scrape_recipes('ah_receps',
                   ah_scraper.base_recipe_url,
                   ah_scraper.recipe_nums)

    print('Scraping Lekker Simpel')
    l_s_scraper = LekkerSimpelScraper()
    l_s_scraper.get_recipes()
    scrape_recipes('ls_receps',
                   l_s_scraper.base_recep_url,
                   l_s_scraper.recipes)

    smull_scraper = SmulwebScraper()
    smull_scraper.get_numbers()
    scrape_recipes('smulweb_receps',
                   smull_scraper.base_recipe_url,
                   smull_scraper.recipe_nums)


if __name__ == '__main__':
    start = time.time()
    main()
    print(f'runtime: {time.time() - start}s')

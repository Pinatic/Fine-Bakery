from albert_scraperV2 import AlbertScraper
from lekker_simpel_scraper import LekkerSimpelScraper 
import time

# import sys
# import codecs
# sys.stdout = codecs.getwriter('utf8')(sys.stdout)

def main():
    # print('Scraping Albert Hein')
    # ah_scraper = AlbertScraper()
    # ah_scraper.get_numbers()
    # ah_scraper.scrape_recipes()

    print('Scraping Lekker Simpel')
    l_s_scraper = LekkerSimpelScraper()
    l_s_scraper.get_recipes()
    l_s_scraper.scrape_recipes()



if __name__ == '__main__':
    start = time.time()
    main()
    print(f'runtime: {time.time() - start}s')

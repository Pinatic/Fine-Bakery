import requests
import re
from recipe_scrapers import scrape_me
from datetime import datetime


class AlbertScraper:
    """
    Scrapes recieps from https://www.ah.nl/allerhande/
    By: Jacob Menzinga
    """
    def __init__(self) -> None:
        self.base_url = 'https://www.ah.nl/allerhande/recepten-zoeken?page='
        self.recipe_nums = None
        self.output_path = f"ah_{datetime.today().strftime('%Y-%m-%d')}.csv"

    def get_numbers(self):
        """
        Retrives all the recipe numbers from a range of AH recipe pages
        """

        pattern = 'R-R(\d{6,7})'
        numbers = []
        page_num = 0

        # while True:
        while page_num < 2:  # For testing, to replace with while true
            print(f'Page {page_num}')

            # getting HTML
            r = requests.get(f'{self.base_url}{page_num}')

            # checking if there's still recipes on the page
            if 'R-R' not in r.text:
                break

            else:
                numbers += set(re.findall(pattern=pattern, string=r.text))
                page_num += 1

        self.recipe_nums = numbers

    def scrape_recipes(self):
        """
        Scrapes all the recipes found in the get_numbers functions and
        stores them in a CSV
        """
        # writing the header
        with open(self.output_path, 'a') as output:
            output.write("title,ingredients,directions,linksource,NER\n")

            # Setting up a counter so we can track progress
            n = 1

            for recp_num in self.recipe_nums[:5]:
                scraper = scrape_me(f'https://www.ah.nl/allerhande/recept/R-R{recp_num}')

                title = scraper.title()
                ingredients = scraper.ingredients()
                instructions = scraper.instructions_list()
                url = scraper.url

                output.write(f'{title},"{ingredients}","{instructions}",{url},\n')

                print(f'{n} recipes scraped')
                n += 1

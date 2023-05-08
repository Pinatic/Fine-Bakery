import requests
import re
# import time


class SmulwebScraper:
    """
    Scrapes recieps from https://www.smulweb.nl
    By: Jacob Menzinga
    """
    def __init__(self) -> None:
        self.base_search_url = 'https://www.smulweb.nl/recepten?page='
        self.base_recipe_url = 'https://www.smulweb.nl/recepten/'
        self.recipe_nums = None

    def get_numbers(self):
        """
        Retrives all the recipe numbers from a range of lekker simpel
        recipe pages
        """

        pattern = '/(\d{7})/'
        numbers = []
        page_num = 1

        # while True:
        while True:
            print(f'Page {page_num}')

            # getting HTML
            r = requests.get(f'{self.base_search_url}{page_num}')

            # checking if there's still recipes on the page
            if 'Geen zoekresultaten gevonden.' in r.text:
                break

            else:
                numbers += set(re.findall(pattern=pattern, string=r.text))
                page_num += 1

        unique_nums = set(numbers)

        self.recipe_nums = list(unique_nums)

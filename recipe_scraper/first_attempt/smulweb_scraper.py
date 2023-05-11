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

    def get_numbers(self, start_at=1):
        """
        Retrives all the recipe numbers from a range of lekker simpel
        recipe pages
        """

        pattern = '/(\d{7})/'
        page_num = start_at

        with open('smulweb_recep_nrs.csv', 'a') as recep_file:

            while True:
                print(f'Page {page_num}')

                # getting HTML
                r = requests.get(f'{self.base_search_url}{page_num}')

                # checking if there's still recipes on the page
                if 'Geen zoekresultaten gevonden.' in r.text:
                    break

                else:
                    numbers = re.findall(pattern=pattern, string=r.text)
                    recep_file.write(f'{page_num},"{str(numbers)}"\n')

                    page_num += 1


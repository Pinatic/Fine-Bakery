import requests
import re

class AlbertScraper:
    """
    Scrapes recieps from https://www.ah.nl/allerhande/
    By: Jacob Menzinga
    """
    def __init__(self) -> None:
        self.base_search_url = 'https://www.ah.nl/allerhande/recepten-zoeken?page='
        self.base_recipe_url = 'https://www.ah.nl/allerhande/recept/R-R'
        self.recipe_nums = None

    def get_numbers(self):
        """
        Retrives all the recipe numbers from a range of AH recipe pages
        """

        pattern = 'R-R(\d{6,7})'
        numbers = []
        page_num = 0

        # while True:
        while True:  # For testing, to replace with while true
            print(f'Page {page_num}')

            # getting HTML
            r = requests.get(f'{self.base_search_url}{page_num}')

            # checking if there's still recipes on the page
            if 'R-R' not in r.text:
                break

            else:
                numbers += set(re.findall(pattern=pattern, string=r.text))
                page_num += 1

        self.recipe_nums = numbers

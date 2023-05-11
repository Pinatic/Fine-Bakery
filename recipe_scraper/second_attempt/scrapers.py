import requests
from bs4 import BeautifulSoup
import re
import json
import os
import pandas as pd
import numpy as np
from recipe_scrapers import scrape_me
import csv


class LekkerEnSimpelScraper:
    """
    Scrapes all the recipes of lekkersimpel.com
    """

    def __init__(self) -> None:
        self.recipes = None
        self.base_recipe_url = 'https://www.lekkerensimpel.com/'

    def get_recipes(self, destination, start_at=1):
        """
        Goes through all the pages of all the food categories and stores the
        recipes in a list. Any duplicates are removed from this list and then
        it gets saved as a object variable.
        """
        tags = ['ontbijtrecepten', 'lunchrecepten', 'tussendoortjes',
                'voorgerecht', 'hoofdgerechten', 'bijgerechten',
                'nagerechten', 'salades', 'bakken']

        recipes = []

        if not os.path.exists(destination):
            os.makedirs(destination)

        with open(destination+'smulweb_recep_nrs.txt', 'w') as recep_file:
            with open(destination+'smulweb_page_nr_reached.txt', 'w') as page_storer:

                for tag in tags[:2]:
                    print(f'working on {tag}')
                    page_num = start_at
                    page_url = f'https://www.lekkerensimpel.com/{tag}/page/{page_num}/'

                    while page_num < 5:
                        print(f'page number: {page_num}')
                        html = requests.get(page_url)

                        if 'class="cell large-6 medium-6 small-12"' in html.text:

                            soup = BeautifulSoup(html.text, 'html.parser')

                            [recipes.append(a['href'].split('/')[-2]) for a in
                             (soup.find_all('a', attrs={"class": "post-item__anchor"}))]

                            page_num += 1

                        else:
                            break

                self.recipes = list(set(recipes))

    def get_numbers(self, destination, start_at=1):
        """
        Retrives all the recipe numbers from a range of lekker simpel
        recipe pages
        """

        pattern = '/(\d{7})/'
        page_num = start_at
        if not os.path.exists(destination):
            os.makedirs(destination)

        with open(destination+'ls_recep_nrs.txt', 'w') as recep_file:
            with open(destination+'ls_page_nr_reached.txt', 'w') as page_storer:

                while page_num < 3:  # True for production
                    print(f'Page {page_num}')

                    # getting HTML
                    r = requests.get(f'{self.base_search_url}{page_num}')

                    # checking if there's still recipes on the page
                    if 'Geen zoekresultaten gevonden.' in r.text:
                        break

                    else:
                        numbers = re.findall(pattern=pattern, string=r.text)
                        recep_file.write(str(numbers).strip('"[]'))
                        page_storer.write(str(page_num)+'\n')
                    page_num += 1


class AlbertScraper:
    """
    Scrapes recieps from https://www.ah.nl/allerhande/
    By: Jacob Menzinga
    """

    def __init__(self) -> None:
        self.base_search_url = 'https://www.ah.nl/allerhande/recepten-zoeken?page='
        self.base_recipe_url = 'https://www.ah.nl/allerhande/recept/R-R'
        self.recipe_nums = None

    # def get_numbers(self):
    #     """
    #     Retrives all the recipe numbers from a range of AH recipe pages
    #     """

        # pattern = 'R-R(\d{6,7})'
        # numbers = []
        # page_num = 0

        # # while True:
        # while True:  # For testing, to replace with while true
        #     print(f'Page {page_num}')

        #     # getting HTML
        #     r = requests.get(f'{self.base_search_url}{page_num}')

        #     # checking if there's still recipes on the page
        #     if 'R-R' not in r.text:
        #         break

        #     else:
        #         numbers += set(re.findall(pattern=pattern, string=r.text))
        #         page_num += 1

        # self.recipe_nums = numbers

    def get_numbers(self, destination, start_at=0):
        """
        Retrives all the recipe numbers from a range of lekker simpel
        recipe pages
        """

        pattern = 'R-R(\d{6,7})'
        page_num = start_at

        if not os.path.exists(destination):
            os.makedirs(destination)

        with open(destination+'ah_recep_nrs.txt', 'w') as recep_file:
            with open(destination+'ah_page_nr_reached.txt', 'w') as page_storer:

                while page_num < 3:  # True for production
                    print(f'Page {page_num}')

                    # getting HTML
                    r = requests.get(f'{self.base_search_url}{page_num}')

                    # checking if there's still recipes on the page
                    if 'Geen zoekresultaten gevonden.' in r.text:
                        break

                    else:
                        numbers = re.findall(pattern=pattern, string=r.text)
                        recep_file.write(str(numbers).strip('"[]'))
                        page_storer.write(str(page_num)+'\n')
                    page_num += 1


class SmulwebScraper:
    """
    Scrapes recieps from https://www.smulweb.nl
    By: Jacob Menzinga
    """

    def __init__(self) -> None:
        self.base_search_url = 'https://www.smulweb.nl/recepten?page='
        self.base_recipe_url = 'https://www.smulweb.nl/recepten/'
        self.recipe_nums = None

    def get_numbers(self, destination, start_at=1):
        """
        Retrives all the recipe numbers from a range of lekker simpel
        recipe pages
        """

        pattern = '/(\d{7})/'
        page_num = start_at
        if not os.path.exists(destination):
            os.makedirs(destination)

        with open(destination+'smulweb_recep_nrs.txt', 'w') as recep_file:
            with open(destination+'smulweb_page_nr_reached.txt', 'w') as page_storer:

                while page_num < 3:  # True for production
                    print(f'Page {page_num}')

                    # getting HTML
                    r = requests.get(f'{self.base_search_url}{page_num}')

                    # checking if there's still recipes on the page
                    if 'Geen zoekresultaten gevonden.' in r.text:
                        break

                    else:
                        numbers = re.findall(pattern=pattern, string=r.text)
                        recep_file.write(str(numbers).strip('"[]'))
                        page_storer.write(str(page_num)+'\n')
                    page_num += 1


class scrape_recipes:
    """
    Scrapes all the recipes found in a list of recipe urls and stores them in
    seperate json files using the recipe name in the supplied list as name

    attributes:
    folder (str): The location where the recipes should be stored
    base_url (str): The base url that refers to the website you want to scrape
    recipe_num_txt (csv file): A csv file containing the page,list of recipes of a
    scraped site
    """

    def __init__(self, folder, base_url, recipe_num_txt) -> None:
        self.folder = folder
        self.base_url = base_url
        self.recipe_num_txt = recipe_num_txt
        self.recipe_list = None

    def create_list(self):
        with open(self.recipe_num_txt, 'r') as recep_file:
            self.recipe_list = recep_file.readline().replace("'", "").split(',')

    def fetch_receps(self):
        n = 0
        "gets the receps in a recep list"
        for recep in self.recipe_list[:10]:
            filename = '_'.join(recep.lower().split())+'.json'

            if os.path.isfile(self.folder+"/"+filename) is False:
                print(f'{self.base_url}{recep}')
                scraper = scrape_me(f'{self.base_url}{recep}')

                if not os.path.exists(self.folder):
                    os.makedirs(self.folder)

                with open(self.folder+"/"+filename, 'w') as output:
                    js = scraper.to_json()
                    json.dump(js, output, indent=4)

                    # A counter to keep track of the nr of recipes scraped
                    n += 1
                    print(f'{n} recipes scraped')

                    # time.sleep(2)  # To not overask the servers

            else:
                print('Recipe already scraped.')
                continue

# Extend this to include a csv writer i think.

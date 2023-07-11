In this folder you will find the code used to scrape recipes of two dutch recipe websites.
To succesfully scrape recipes you first need to run the get_identifiers.py file. This will create a txt file with all the recipe identifiers of the website we're scraping.
Then you can run get_recipes.py to scrape the recipes. This will create a json file with all the recipes.

At the moment only ah.nl and smulweb are supported. If you want to scrape other websites you need to figure out how to get the recipe identifiers. The code in 'recipe_identifier_fetchers.py' can be used as a starting point. Once you've got the identifiers you can use the 'get_recipes.py' file to scrape the recipes.

In the subfolders are older versions of the scraper, I've left them in for reference. <br>
All code in this and subfolders is written by Jacob Menzinga
If there are any questions you can contact me at jacobmenzinga@gmail.com
..


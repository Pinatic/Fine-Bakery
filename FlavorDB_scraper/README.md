# FlavorDataScraper

FlavorDataScraper is a Python class that enables scraping flavor data from FlavorDB and storing it in a JSON file. 
## Features

- Scrapes flavor data from FlavorDB using JSON files.
- Filters and selects specific columns of interest from the scraped data.
- Stores the filtered flavor data in a JSON file for further analysis.
## Requirements

- Python 3.6+
- pandas
- matplotlib
- colour
- networkx
- mpld3

## Installation

1. Clone the repository:

git clone https://github.com/your-username/FlavorDataScraper.git


2. Install the required dependencies:

pip install pandas matplotlib colour networkx mpld3


## Usage


from FlavorDataScraper import FlavorDataScraper

# Create an instance of FlavorDataScraper
scraper = FlavorDataScraper()

# Scrape flavor data and store it in a JSON file
scraper.scrape_flavor_data()


Running the above code will initiate the flavor data scraping process. The scraped data will be filtered and stored in a JSON file named "ingredients.json".

## Documentation

Please refer to the class docstrings for detailed information on the methods and attributes of the FlavorDataScraper class.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.



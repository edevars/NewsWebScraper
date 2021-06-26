# News Web Scraper 

This is a project developed with Python using the Scrapy framework to do web scraping. This project extracts articles from news websites with target in politics news. The final porpouse of the recolected data is to train a machine learning model.

## Installation

Clone this repository and install the virual environment

```bash
conda env create -f environment.yml 
```

And activate the virtual environment with:

```bash
conda activate NewsWebScraper
```

## Run a spider

All the spiders are located in the spiders folder inside the project.

```bash
scrapy runspider <path_to_spider>
```

## Run all the spiders at the same time

```bash
python ./news_scraper/run_spiders.py
```
# BooksToScrape Web Scraper

This Python script scrapes book information (title, price, availability, and rating)  
from the [BooksToScrape](https://books.toscrape.com/) website, page by page,  
and prints the details in the terminal.

## Features

- Scrapes multiple pages automatically  
- Gets book title, price, availability, and star rating  
- Handles network errors gracefully  
- Polite scraping with a short delay between requests  

## Requirements

- Python 3.x  
- `requests` library  
- `beautifulsoup4` library  

Install dependencies using:

```bash
pip install -r requirements.txt

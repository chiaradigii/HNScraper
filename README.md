# HackerNewsScraper

HackerNewsScraper is a Python tool for scraping the top 30 entries from the Hacker News homepage. This scraper extracts key details such as rank, title, points, and comments for each post. Additionally, it provides functionality to filter these entries based on the number of words in the title and to sort them by either comments or points.

## Features
* Scrape top 30 entries from Hacker News.
* Filter entries with more than or less than or equal to 5 words in their titles.
* Sort entries by the number of comments or points.

## Requirements
Before you begin, ensure you have met the following requirements:

* You have installed the latest version of Python.
* You have installed the necessary Python packages listed in the requirements.txt file.
  You can install them using pip:
  
pip install -r requirements.txt

## Installation and Setup

* Clone the Repository
git clone https://github.com/chiaradigii/HNScraper.git

* Set up a virtual environment and install the required packages:

python -m venv venv

source venv/bin/activate  # On Windows use `venv\Scripts\activate`

pip install -r requirements.txt

## Usage

### To run the scraper:

from scraper import HackerNewsScraper

    scraper = HackerNewsScraper('https://news.ycombinator.com/')
    entries = scraper.scrape()
    print(entries)

### To filter and sort the scraped entries:

filtered_more_than_five = scraper.filter_entries(sort_by='comments', mode='greater')
filtered_five_or_less = scraper.filter_entries(sort_by='points', mode='less_equal')

print("Entries with titles containing more than five words:", filtered_more_than_five)
print("\nEntries with titles containing five or less words:", filtered_five_or_less)

## Testing

This project includes unit tests that cover scraping, filtering, and error handling functionalities. To run the tests:

python -m unittest test_scraper.py

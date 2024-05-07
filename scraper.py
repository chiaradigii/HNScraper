import requests
from bs4 import BeautifulSoup

def scrape_hn_top_entries(url):
    """
    Scrape the top 30 entries from the Hacker News homepage.

    Args:
        url (str): URL to the Hacker News homepage.

    Returns:
        list of dict: A list of dictionaries, each containing the rank, title, points, and comments of a post.
    """
    pass
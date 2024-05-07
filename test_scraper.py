import unittest
from scraper import HackerNewsScraper

class TestHackerNewsScraper(unittest.TestCase):

    def setUp(self):
        self.scraper = HackerNewsScraper('https://news.ycombinator.com/')

    def test_scrape(self):
        result = self.scraper.scrape()
        self.assertIsInstance(result, list, "Result should be a list")
        self.assertTrue(len(result) > 0, "Result should contain more than 0 entries")

    def test_filter_entries(self):
        self.scraper.scrape()  
        filtered_more_than_five = self.scraper.filter_entries('comments', 'greater')
        filtered_five_or_less = self.scraper.filter_entries('points', 'less_equal')

        self.assertIsInstance(filtered_more_than_five, list, "Filtered list should be a list")
        self.assertIsInstance(filtered_five_or_less, list, "Filtered list should be a list")

        for entry in filtered_more_than_five:
            self.assertTrue(len(entry['title'].split()) > 5, "Title should contain more than five words")

        for entry in filtered_five_or_less:
            self.assertTrue(len(entry['title'].split()) <= 5, "Title should contain five or fewer words")

if __name__ == '__main__':
    unittest.main()
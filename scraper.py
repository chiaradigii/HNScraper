import requests
from bs4 import BeautifulSoup
from pprint import pprint

def scrape_hn_top_entries(url):
    """
    Scrape the top 30 entries from the Hacker News homepage.

    Args:
        url (str): URL to the Hacker News homepage.

    Returns:
        list of dict: A list of dictionaries, each containing the rank, title, points, and comments of a post.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # HTTPError is raised if the status is 4xx, 5xx
    except requests.RequestException as e:
        return [{'error': str(e)}]

    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.select('tr.athing')[:30] # Select first 30 entries
        entries = []
        for item in items:
            rank = item.select_one('.rank')
            title = item.select_one('.title a')
            # Parent tr tag contains the subtext with score and comments
            subtext = item.find_next_sibling('tr').select_one('.subtext')
            score = subtext.select_one('.score')
            comments_link = subtext.select_one('a[href^="item?id="]')

            rank = rank.text.strip('.') if rank else 'N/A'
            title = title.text if title else 'No title found'
            points = int(score.text.split()[0]) if score else 0
            comments_text = comments_link.text if comments_link else '0 comments'
            comments = int(comments_text.replace('\xa0', ' ').split()[0])
            entries.append({
                'rank': rank,
                'title': title,
                'points': points,
                'comments': comments
            })
    except Exception as e:
        return [{'error': f"Failed to parse data: {str(e)}"}]

    return entries

url = 'https://news.ycombinator.com/'
entries = scrape_hn_top_entries(url)
#pprint(entries)

def filter_by_title_length(entries, max_words = 5, sort_by = 'comments'):
    """
    Filter all previous entries with no more than five words in the title ordered by the number of comments first.

    Args:
        entries (list of dict): The entries to filter.
        max_words (int): Maximum number of words in the title for filtering. Default is 5.
        sort_by (str): The key to sort the entries by ('comments' is default).

    Returns:
        list of dict: The filtered and sorted list of entries.
    """
    filtered_entries = [entry for entry in entries if len(entry['title'].split())  <= max_words]
    return sorted(filtered_entries, key=lambda x: x[sort_by], reverse=True)

filtered_no_more_than_five = filter_by_title_length(entries, 5, 'comments')

print("Entries with no more than five words in the title sorted by comments:")
pprint(filtered_no_more_than_five)

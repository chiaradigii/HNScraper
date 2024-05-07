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


def filter_entries(entries, sort_by='comments', mode='less_equal'):
    """
    Filter entries based on the number of words in the title and sort them by specific criteria.
    This function filters entries to those with titles containing more than or less than or equal to 5 words,
    depending on the mode specified, and sorts them based on either 'comments' or 'points'.
    
    Args:
        entries (list of dict): The entries to filter.
        sort_by (str): The key to sort the entries by ('comments' is default).

    Returns:
        list of dict: The filtered and sorted list of entries.
    """
    if mode == 'less_equal':
        filtered_entries = [entry for entry in entries if len(entry['title'].split()) <= 5]
    else:
        filtered_entries = [entry for entry in entries if len(entry['title'].split()) > 5]

    return sorted(filtered_entries, key=lambda x: x[sort_by], reverse=True)

url = 'https://news.ycombinator.com/'
entries = scrape_hn_top_entries(url)
#pprint(entries)
filtered_more_than_five = filter_entries(entries, 5, 'comments', 'greater')
filtered_five_or_less = filter_entries(entries, 5, 'points', 'less_equal')

print("Entries with more than five words in the title sorted by comments:")
pprint(filtered_more_than_five)
print("Entries with five or fewer words in the title sorted by points:")
pprint(filtered_five_or_less)

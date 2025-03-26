import requests
import pandas as pd 
import httpx
from bs4 import BeautifulSoup

# Define the session and headers
session = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

#ga_q1
def get_ducks_sum(page_number: int) -> int:
    """
    Fetches the total number of ducks (0 runs) from ESPN Cricinfo's ODI batting statistics for the given page.

    Args:
        page_number (int): The page number to scrape.

    Returns:
        int: The total number of ducks on the specified page.
    """
    url = f"https://stats.espncricinfo.com/stats/engine/stats/index.html?class=2;page={page_number};template=results;type=batting"

    # Fetch the HTML content using the session and headers defined earlier
    response = session.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch data. Status code: {response.status_code}")

    # Read the tables from the HTML content
    tables = pd.read_html(response.text)
    
    # Convert the specific table to DataFrame
    t = pd.DataFrame(tables[2])
    
    # Return the sum of the '0' column
    return t['0'].astype(int).sum()

# Example usage
page_number = 30
print(get_ducks_sum(page_number))

##########################################################################################
#ga_q2



def fetch_imdb_movies(url: str, limit: int = 25) -> list:
    """
    Fetches a list of movies from IMDb based on the given URL and limit.

    Args:
      url (str): The URL to fetch the movies from.
      limit (int): The number of movies to fetch. Default is 25.

    Returns:
      list: A list of dictionaries containing movie details.
    """
    headers = {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"  # Pretend to be a regular browser
    }
    response = httpx.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    movies = soup.find_all("li", class_="ipc-metadata-list-summary-item", limit=limit)

    final_out = []

    for movie in movies:
        temp_dict = {}
        temp_dict['id'] = movie.find("a", class_="ipc-title-link-wrapper").get("href").split('/')[2]
        temp_dict['title'] = movie.find("h3", class_="ipc-title__text").text.strip()
        temp_dict['year'] = movie.find_all("span", class_="sc-f30335b4-7 jhjEEd dli-title-metadata-item")[0].text.strip('-').strip()
        temp_dict['rating'] = movie.find_all("span", class_="ipc-rating-star--rating")[0].text
        final_out.append(temp_dict)

    final_out = [{k: v.replace("–", "") if isinstance(v, str) else v for k, v in movie.items()} for movie in final_out]
    return final_out

# Example usage
url = "https://www.imdb.com/search/title/?user_rating=2,6"
movies = fetch_imdb_movies(url)
print(movies)

#############################################################################################################################################
#ga_q6



def fetch_most_recent_link(keyword: str, points: int) -> str:
    """
    Fetches the most recent link from Hacker News RSS feed based on the given keyword and minimum points.

    Args:
        keyword (str): The keyword to search for in the RSS feed.
        points (int): The minimum points required for the articles.

    Returns:
        str: The most recent link from the RSS feed that matches the criteria.
    """
    # Construct the RSS feed URL
    rss_url = f"https://hnrss.org/newest?q={keyword}&points>{points}"

    # Fetch the RSS feed
    response = httpx.get(rss_url)
    response.raise_for_status()

    # Parse the RSS feed
    soup = BeautifulSoup(response.text)

    # Find the most recent <item>
    most_recent_item = soup.find('item')

    # Extract the <link> tag inside the most recent <item>
    most_recent_link = most_recent_item.find('link').next_sibling.strip()

    return most_recent_link

# Example usage
keyword = "WebAssembly"
points = 49
print(fetch_most_recent_link(keyword, points))

#############################################################################################################################################

#ga_q9


#############################################################################################################################################

#g_q6




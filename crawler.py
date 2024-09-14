import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

# Set of common redirection parameters
REDIRECT_PARAMS = ['redirect', 'url', 'next', 'target']

# Custom headers to mimic a real browser request
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

# ASCII art of a man in a balaclava
def display_ascii_art():
    balaclava_art = """
     ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣴⣶⣾⣿⣿⣶⣦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
     ⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣄⠀⠀⠀⠀⠀⠀⠀
     ⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆⠀⠀⠀⠀⠀
     ⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀⠀
     ⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⡿⠿⠛⠛⠛⠛⠻⢿⣿⣿⣿⣿⡀⠀⠀
     ⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⡿⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⡇⠀⠀
     ⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⠏⠀⠀⠀⠀⢀⣠⣤⣤⣀⠀⠀⠀⠈⣿⣿⡇⠀⠀
     ⠀⠀⠀⠀⠀⠀⠸⣿⣿⡇⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿⣄⠀⠀⢹⣿⠇⠀⠀
     ⠀⠀⠀⠀⠀⠀⠀⠘⣿⣧⠀⠀⢀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⣿⠀⠀⠀
     ⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣇⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣼⡟⠀⠀⠀
     ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀
     ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠻⠿⠿⠿⠿⣿⣿⣿⣿⡿⠁⠀⠀⠀⠀⠀
     """
    print(balaclava_art)

def get_links_from_page(url):
    """
    Fetches and parses all the URLs from a given page.
    """
    try:
        # Send a request to the URL with custom headers
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()  # Raise an exception for bad responses
        
        # Parse the page content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Collect all the links from the page
        links = set()
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            full_url = urljoin(url, href)  # Handle relative URLs
            print(f"Found link: {full_url}")  # Print every link found
            links.add(full_url)
        return links

    except requests.RequestException as e:
        print(f"Error accessing {url}: {e}")
        return set()

def find_redirect_urls(links):
    """
    Filters and returns URLs containing redirection parameters.
    """
    redirect_urls = []
    
    for link in links:
        parsed_url = urlparse(link)
        query_params = parsed_url.query.split('&')
        
        # Check if any redirection parameter exists in the URL's query
        for param in query_params:
            key_value = param.split('=')
            if len(key_value) == 2 and key_value[0].lower() in REDIRECT_PARAMS:
                redirect_urls.append(link)
                break
    
    return redirect_urls

def crawl_and_find_redirects(start_url):
    """
    Crawls a given website and finds URLs containing redirection parameters.
    """
    print(f"Crawling website: {start_url}")
    all_links = get_links_from_page(start_url)
    redirect_urls = find_redirect_urls(all_links)
    
    if redirect_urls:
        print(f"\nFound URLs with redirection parameters:")
        for redirect_url in redirect_urls:
            print(redirect_url)
    else:
        print("\nNo URLs with redirection parameters found.")

if __name__ == "__main__":
    # Display the balaclava ASCII art
    display_ascii_art()
    
    # Input the website URL to crawl
    website_url = input("Enter website URL to crawl: ")
    crawl_and_find_redirects(website_url)

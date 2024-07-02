import requests
from bs4 import BeautifulSoup

def fetch_listing(url: str, timeout: int = 10) -> str:
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        soup = BeautifulSoup(response.text, 'html.parser')
        body_text = soup.body.get_text(strip=True)
        return body_text
    except requests.RequestException as error:
        print('Error fetching the URL:', error)
        raise

import aiohttp
from bs4 import BeautifulSoup

async def fetch_listing(url: str, timeout: int = 10) -> str:
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=timeout) as response:
                response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                body_text = soup.body.get_text(strip=True)
                return body_text
        except aiohttp.ClientError as error:
            print('Error fetching the URL:', error)
            raise